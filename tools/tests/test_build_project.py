import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build_project as bp

EXAMPLE=Path(__file__).resolve().parents[2]/'projects'/'obra-com-mezanino'/'model.json'


class ProjectGenerationTest(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(EXAMPLE.read_text(encoding='utf-8'))

    def test_r04_numbered_members_and_mezzanine_landing(self):
        self.assertEqual(bp.validate(self.data),(5000.,6000.,5600.))
        self.assertEqual(len(self.data['elementos']),42)
        self.assertEqual(self.data['revisao'],'R04')
        self.assertEqual({e['tipo'] for e in self.data['elementos']},{'face','caixa'})
        self.assertEqual(sum(1 for e in self.data['elementos'] if e['tag']=='PILARES_ESTUDO'),6)
        self.assertEqual(sum(1 for e in self.data['elementos'] if e['tag']=='PILARES_MEZ_ESTUDO'),3)
        self.assertEqual(sum(1 for e in self.data['elementos'] if e['tag']=='VIGAS_MEZ_ESTUDO'),7)
        self.assertEqual(sum(1 for e in self.data['elementos'] if e['tag']=='TRAVESSAS_BALANCO_ESTUDO'),18)
        self.assertFalse(any(e['id'] in ('P_PF','P_PM','P_PT','V_COB_P') for e in self.data['elementos']))
        self.assertTrue(any(e['id']=='COB_R03' for e in self.data['elementos']))
        self.assertEqual({e['id'] for e in self.data['elementos'] if e['tag']=='PILARES_ESTUDO'}, set('C%02d'%i for i in range(1,7)))
        self.assertEqual({e['id'] for e in self.data['elementos'] if e['tag']=='PILARES_MEZ_ESTUDO'}, set('C%02d'%i for i in range(7,10)))
        self.assertEqual(len([e for e in self.data['elementos'] if e['id'].startswith('V07_')]),6)
        self.assertEqual(self.data['parametros_estudo_mm']['mezanino_r04']['area_total_m2'],16.8)
        p = next(e for e in self.data['elementos'] if e['id']=='MEZ_PRINCIPAL')
        l = next(e for e in self.data['elementos'] if e['id']=='MEZ_PATAMAR')
        self.assertEqual(p['origem_mm'], [1000,1000,2690])
        self.assertEqual(p['dimensoes_mm'], [3000,5000,160])
        self.assertEqual(l['origem_mm'], [0,4200,2690])
        self.assertEqual(l['dimensoes_mm'], [1000,1800,160])
        stair = next(e for e in self.data['elementos'] if e['id']=='ESCADA_RES')
        self.assertEqual(max(v[1] for v in stair['pontos_mm']),4200)
        self.assertEqual(min(v[0] for v in stair['pontos_mm']),100)
        self.assertEqual(self.data['parametros_estudo_mm']['balanco_direito']['balanco_nominal'],1000)

    def test_dxf_ascii_r12_contains_geometry(self):
        for view in ('planta','elevacoes'):
            dxf=bp.dxf(self.data,view)
            self.assertIn(b'AC1009',dxf)
            self.assertIn(b'\nLINE\n',dxf)
            self.assertTrue(dxf.endswith(b'\nEOF\n'))
            self.assertIn(b'OFICINA_REFERENCIA',dxf)
        self.assertIn(b'6000',bp.dxf(self.data,'planta'))
        plan = bp.dxf(self.data,'planta')
        self.assertIn(b'\nC01\n',plan)
        self.assertIn(b'\nC09\n',plan)
        self.assertIn(b'\nV01\n',plan)
        self.assertIn(b'\nV09\n',plan)
        self.assertIn(b'\nV12\n',plan)

    def test_collada_valid_xml_and_metric_units(self):
        tree=ET.fromstring(bp.dae(self.data))
        ns={'c':bp.NS}
        self.assertEqual(tree.find('.//c:unit',ns).attrib['meter'],'0.001')
        self.assertEqual(tree.find('.//c:up_axis',ns).text,'Z_UP')
        nodes=tree.findall('.//c:visual_scene/c:node',ns)
        self.assertEqual(len(nodes),42)
        triangles=tree.findall('.//c:mesh/c:triangles',ns)
        self.assertEqual(sum(int(tr.attrib['count']) for tr in triangles),284)

    def test_rejects_missing_units(self):
        self.data['unidades']='m'
        with self.assertRaisesRegex(ValueError,'Schema/unidades'):bp.validate(self.data)

    def test_rejects_nan(self):
        self.data['elementos'][1]['pontos_mm'][1][1]=float('nan')
        with self.assertRaises(ValueError):bp.validate(self.data)

    def test_rejects_extra_element_outside_envelope(self):
        self.data['elementos'][1]['pontos_mm'][1][0]=5001
        with self.assertRaisesRegex(ValueError,'fora do envelope'):bp.validate(self.data)

    def test_rejects_corrupt_envelope(self):
        self.data['envelope_mm']['z']=6000
        with self.assertRaisesRegex(ValueError,'incoerente'):bp.validate(self.data)

    def test_rejects_duplicate_id(self):
        self.data['elementos'][1]['id']=self.data['elementos'][0]['id']
        with self.assertRaisesRegex(ValueError,'duplicado'):bp.validate(self.data)

    def test_rejects_non_coplanar_face(self):
        next(e for e in self.data['elementos'] if e['id']=='V09_ENDR')['pontos_mm'][0][0]-=45
        with self.assertRaisesRegex(ValueError,'nao coplanar'):bp.validate(self.data)

    def test_build_manifest_integrity_and_check_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'obra-com-mezanino'/'model.json'
            path.parent.mkdir()
            path.write_bytes(EXAMPLE.read_bytes())
            first=bp.build(path)
            self.assertTrue(bp.build(path,check=True))
            manifest=json.loads((path.parent/'manifest.json').read_text())
            self.assertEqual(manifest['schema'],bp.SYNC_SCHEMA)
            self.assertEqual(len(manifest['files']),4)
            for rel,meta in manifest['files'].items():
                content=(path.parent/rel).read_bytes()
                self.assertEqual(meta['sha256'],hashlib.sha256(content).hexdigest())
                self.assertEqual(meta['size'],len(content))
            (path.parent/'cadcraft'/'planta.dxf').write_text('TAMPERED')
            with self.assertRaisesRegex(ValueError,'desatualizado'):bp.build(path,check=True)

    def test_deterministic_outputs(self):
        generated_1=(bp.dxf(self.data,'planta'),bp.dxf(self.data,'elevacoes'),bp.dae(self.data))
        generated_2=(bp.dxf(copy.deepcopy(self.data),'planta'),bp.dxf(copy.deepcopy(self.data),'elevacoes'),bp.dae(copy.deepcopy(self.data)))
        self.assertEqual(generated_1,generated_2)

    def test_regenerated_files_match_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'obra-com-mezanino'/'model.json'
            path.parent.mkdir()
            path.write_bytes(EXAMPLE.read_bytes())
            bp.build(path)
            self.assertTrue(bp.build(path,check=True))

if __name__=='__main__':unittest.main()
