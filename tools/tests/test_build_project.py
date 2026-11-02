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

    def test_r09_five_150x150x3_columns_and_beam_V13(self):
        self.assertEqual(bp.validate(self.data),(10461.,37341.,5600.))
        self.assertEqual(len(self.data['elementos']),52)
        self.assertEqual(self.data['revisao'],'R09')
        self.assertEqual({e['tipo'] for e in self.data['elementos']},{'face','caixa'})
        self.assertEqual(sum(1 for e in self.data['elementos'] if e['tag']=='PILARES_ESTUDO'),7)
        self.assertEqual(sum(1 for e in self.data['elementos'] if e['tag']=='PILARES_MEZ_ESTUDO'),2)
        self.assertEqual(sum(1 for e in self.data['elementos'] if e['tag']=='VIGAS_MEZ_ESTUDO'),7)
        self.assertEqual(sum(1 for e in self.data['elementos'] if e['tag']=='TRAVESSAS_BALANCO_ESTUDO'),24)
        self.assertFalse(any(e['id'] in ('P_PF','P_PM','P_PT','V_COB_P') for e in self.data['elementos']))
        self.assertTrue(any(e['id']=='COB_R03' for e in self.data['elementos']))
        self.assertEqual({e['id'] for e in self.data['elementos'] if e['tag']=='PILARES_ESTUDO'}, set('C%02d'%i for i in range(1,7)) | {'C10'})
        self.assertEqual({e['id'] for e in self.data['elementos'] if e['tag']=='PILARES_MEZ_ESTUDO'}, {'C07','C08'})
        self.assertEqual(len([e for e in self.data['elementos'] if e['id'].startswith('V07_')]),6)
        self.assertEqual(self.data['parametros_estudo_mm']['mezanino_r04']['area_total_m2'],16.8)
        p = next(e for e in self.data['elementos'] if e['id']=='MEZ_PRINCIPAL')
        l = next(e for e in self.data['elementos'] if e['id']=='MEZ_PATAMAR')
        self.assertEqual(p['origem_mm'], [6461,621,2825])
        self.assertEqual(p['dimensoes_mm'], [3000,4975,25])
        self.assertEqual(l['origem_mm'], [9461,621,2825])
        self.assertEqual(l['dimensoes_mm'], [1000,1800,25])
        stair = next(e for e in self.data['elementos'] if e['id']=='ESCADA_RES')
        self.assertEqual(max(v[1] for v in stair['pontos_mm']),6621)
        self.assertEqual(min(v[0] for v in stair['pontos_mm']),9461)
        self.assertEqual(self.data['parametros_estudo_mm']['balanco_direito']['balanco_nominal'],1000)


    def test_r09_only_floor_changed_since_R08(self):
        previous=json.loads((EXAMPLE.parent/'historico'/'model-R08.json').read_text(encoding='utf-8'))
        self.assertEqual(previous['revisao'],'R08')
        self.assertEqual(len(previous['elementos']),52)
        current={e['id']:e for e in self.data['elementos']}
        before={e['id']:e for e in previous['elementos']}
        self.assertEqual(set(current),set(before))
        for id,old in before.items():
            if id not in ('MEZ_PRINCIPAL','MEZ_PATAMAR'):
                self.assertEqual(current[id],old,id)
        p=current['MEZ_PRINCIPAL']; l=current['MEZ_PATAMAR']
        self.assertEqual(p['origem_mm'],[6461,621,2825])
        self.assertEqual(p['dimensoes_mm'],[3000,4975,25])
        self.assertEqual(l['origem_mm'],[9461,621,2825])
        self.assertEqual(l['dimensoes_mm'],[1000,1800,25])
        self.assertEqual(p['origem_mm'][2]+p['dimensoes_mm'][2],2850)
        self.assertEqual(l['origem_mm'][2]+l['dimensoes_mm'][2],2850)
        self.assertEqual(p['origem_mm'][1]+p['dimensoes_mm'][1],5596)
        self.assertEqual(current['VF08_SUP_ESQ']['pontos_mm'][0][1],5621)
        self.assertEqual(current['VF08_SUP_DIR']['pontos_mm'][0][1],5621)
        self.assertEqual(current['VF08_SUP_ESQ']['pontos_mm'][0][2],2850)
        self.assertEqual(current['VF08_SUP_DIR']['pontos_mm'][0][2],2850)
        self.assertEqual(self.data['parametros_estudo_mm']['piso_r09']['afastamento_geometrico_piso_vidro_mm'],25)
        self.assertEqual(self.data['parametros_estudo_mm']['piso_r09']['intervalo_sem_detalhe_secundario_mm'],135)
        self.assertFalse(self.data['parametros_estudo_mm']['piso_r09']['espessura_estrutural_calculada'])
        self.assertEqual(current['COB_R03'],before['COB_R03'])
        self.assertEqual(current['V05'],before['V05'])
        self.assertEqual(current['C07'],before['C07'])

    def test_r06_preserves_terrain_and_roof_from_r05(self):
        previous=json.loads((EXAMPLE.parent/'historico'/'model-R05.json').read_text(encoding='utf-8'))
        self.assertEqual(previous['revisao'],'R05')
        self.assertEqual(len(previous['elementos']),44)
        self.assertEqual(self.data['envelope_mm'],previous['envelope_mm'])
        refs={e['id']:e for e in self.data['elementos']}
        self.assertEqual(refs['T01_TERRENO'],next(e for e in previous['elementos'] if e['id']=='T01_TERRENO'))
        self.assertEqual(refs['MURO_BC'],next(e for e in previous['elementos'] if e['id']=='MURO_BC'))
        self.assertEqual(refs['PASSE'],next(e for e in previous['elementos'] if e['id']=='PASSE'))
        self.assertEqual(refs['COB_R03'],next(e for e in previous['elementos'] if e['id']=='COB_R03'))
        for prior in previous['elementos']:
            if prior['id'] in ('C02','C03','C04','C05','C06','C07','C09','V05','MEZ_PRINCIPAL','MEZ_PATAMAR'):
                continue
            self.assertEqual(refs[prior['id']],prior)
        self.assertNotIn('C09',refs)
        self.assertEqual(self.data['referencias_estruturais']['aliases_historicos']['C09'],'C04')
        self.assertEqual(self.data['parametros_estudo_mm']['implantacao_r05']['muro_BC']['altura_mm'],4800)
        self.assertEqual(self.data['parametros_estudo_mm']['implantacao_r05']['recuo_frontal_direito_nominal_mm'],300)

    def test_r06_column_alignment_and_six_face_sloped_beam(self):
        refs={e['id']:e for e in self.data['elementos']}
        self.assertEqual(refs['C04']['origem_mm'],[6461,5521,0])
        self.assertEqual(refs['C04']['dimensoes_mm'],[150,150,5225])
        self.assertEqual(refs['C10']['origem_mm'],[10361,5521,0])
        self.assertEqual(refs['C10']['dimensoes_mm'],[100,100,5420])
        self.assertEqual(refs['C04']['tag'],'PILARES_ESTUDO')
        self.assertEqual(refs['C10']['tag'],'PILARES_ESTUDO')
        parts={'SIDEA','SIDEB','TOP','BOTTOM','ENDL','ENDR'}
        for part in parts:
            item=refs['V13_'+part]
            self.assertEqual(item['tipo'],'face')
            self.assertEqual(item['numero_logico'],'V13')
            self.assertEqual(item['tag'],'TRAVESSAS_BALANCO_ESTUDO')
            self.assertEqual({p[1] for p in item['pontos_mm']}.issubset({5521,5621}),True)
            self.assertTrue(all(6461<=p[0]<=10461 for p in item['pontos_mm']))
            self.assertTrue(all(5210<=p[2]<=5585 for p in item['pontos_mm']))
        self.assertIn([6461,5621,5385],refs['V13_TOP']['pontos_mm'])
        self.assertIn([10461,5621,5585],refs['V13_TOP']['pontos_mm'])
        self.assertIn([6461,5521,5210],refs['V13_BOTTOM']['pontos_mm'])
        self.assertIn([10461,5521,5410],refs['V13_BOTTOM']['pontos_mm'])
        self.assertEqual(self.data['parametros_estudo_mm']['estrutura_r06']['viga_V13']['apoios'],['C04','C10'])
        self.assertFalse(any(e['id']=='C09' for e in self.data['elementos']))

    def test_dxf_ascii_r12_contains_geometry(self):
        for view in ('planta','elevacoes'):
            dxf=bp.dxf(self.data,view)
            self.assertIn(b'AC1009',dxf)
            self.assertIn(b'\nLINE\n',dxf)
            self.assertTrue(dxf.endswith(b'\nEOF\n'))
            self.assertIn(b'OFICINA_REFERENCIA',dxf)
        self.assertIn(b'37341',bp.dxf(self.data,'planta'))
        plan = bp.dxf(self.data,'planta')
        self.assertIn(b'\nC01\n',plan)
        self.assertNotIn(b'\nC09\n',plan)
        self.assertIn(b'\nC10\n',plan)
        self.assertIn(b'\nV13\n',plan)
        self.assertIn(b'\nV01\n',plan)
        self.assertIn(b'\nV09\n',plan)
        self.assertIn(b'\nV12\n',plan)
        self.assertIn(b'VIDRO_FUNDOS_ESTUDO',plan)
        self.assertIn(b'T01_TERRENO',plan)
        self.assertIn(b'T01_MURO_BC',plan)

    def test_collada_valid_xml_and_metric_units(self):
        tree=ET.fromstring(bp.dae(self.data))
        ns={'c':bp.NS}
        self.assertEqual(tree.find('.//c:unit',ns).attrib['meter'],'0.001')
        self.assertEqual(tree.find('.//c:up_axis',ns).text,'Z_UP')
        nodes=tree.findall('.//c:visual_scene/c:node',ns)
        self.assertEqual(len(nodes),52)
        triangles=tree.findall('.//c:mesh/c:triangles',ns)
        self.assertEqual(sum(int(tr.attrib['count']) for tr in triangles),304)

    def test_rejects_missing_units(self):
        self.data['unidades']='m'
        with self.assertRaisesRegex(ValueError,'Schema/unidades'):bp.validate(self.data)

    def test_rejects_nan(self):
        self.data['elementos'][1]['pontos_mm'][1][1]=float('nan')
        with self.assertRaises(ValueError):bp.validate(self.data)

    def test_rejects_extra_element_outside_envelope(self):
        self.data['elementos'][1]['pontos_mm'][1][0]=10462
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
