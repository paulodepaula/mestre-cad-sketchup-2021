import copy
import hashlib
import json
import tempfile
import unittest
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build_project as bp
EXAMPLE=Path(__file__).resolve().parents[2]/'projects'/'obra-com-mezanino'/'model.json'

class ProjectGenerationTest(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(EXAMPLE.read_text(encoding='utf-8'))
        self.refs={e['id']:e for e in self.data['elementos']}
        self.prior=json.loads((EXAMPLE.parent/'historico'/'model-R09.json').read_text(encoding='utf-8'))
        self.new=[e for e in self.data['elementos'] if e['id'] not in {x['id'] for x in self.prior['elementos']}]

    def test_r10_contract_and_importer_limits(self):
        self.assertEqual(self.data['revisao'],'R10')
        self.assertEqual(bp.validate(self.data),(10461.,37341.,5600.))
        self.assertEqual(len(self.refs),80)
        self.assertEqual(len(self.new),28)
        self.assertEqual(sum(e['tipo']=='caixa' for e in self.refs.values()),48)
        self.assertEqual(sum(e['tipo']=='face' for e in self.refs.values()),32)
        self.assertTrue(all(len(e['nome'])<=120 and len(e['tag'])<=40 for e in self.refs.values()))

    def test_preserve_all_original_geometry_and_tube_specs(self):
        self.assertEqual(self.prior['revisao'],'R09')
        self.assertEqual(len(self.prior['elementos']),52)
        for old in self.prior['elementos']:
            new=self.refs[old['id']]
            for key in ('tipo','tag','origem_mm','dimensoes_mm','pontos_mm','perfil_referencia','numero_logico'):
                self.assertEqual(new.get(key),old.get(key),(old['id'],key))
        for code in ('C02','C03','C04','C05','C06'):
            self.assertEqual(self.refs[code]['perfil_referencia']['parede_mm'],3)
        self.assertNotIn('C09',self.refs)
        self.assertEqual(self.data['referencias_estruturais']['aliases_historicos']['C09'],'C04')

    @staticmethod
    def bounds(item):
        lo=item['origem_mm'];return lo,[v+d for v,d in zip(lo,item['dimensoes_mm'])]

    @classmethod
    def overlap(cls,a,b):
        al,ah=cls.bounds(a);bl,bh=cls.bounds(b)
        return [min(ah[j],bh[j])-max(al[j],bl[j]) for j in range(3)]

    def test_new_members_do_not_intersect_each_other_or_columns(self):
        cols=[e for e in self.prior['elementos'] if e['tipo']=='caixa' and e['id'].startswith('C')]
        for i,a in enumerate(self.new):
            for b in self.new[i+1:]+cols:
                self.assertFalse(all(x>1e-6 for x in self.overlap(a,b)),(a['id'],b['id']))

    def test_no_floating_frame_members(self):
        prim=[e for e in self.prior['elementos'] if e['tag']=='VIGAS_MEZ_ESTUDO']
        reachable={e['id'] for e in prim}
        all_boxes=prim+self.new
        while True:
            found=set()
            for a in all_boxes:
                if a['id'] in reachable:continue
                for b in all_boxes:
                    if b['id'] not in reachable:continue
                    lengths=self.overlap(a,b)
                    if min(lengths)>=-1e-6 and sum(x>1e-6 for x in lengths)>=2:
                        found.add(a['id']);break
            if not found:break
            reachable.update(found)
        self.assertTrue(all(e['id'] in reachable for e in self.new),[e['id'] for e in self.new if e['id'] not in reachable])

    def test_frame_and_floor_z_contact(self):
        for e in self.new:
            lo,hi=self.bounds(e)
            if e['tag']=='SOLEIRA_VIDRO':
                self.assertEqual((lo[2],hi[2]),(2825,2850))
            else:self.assertEqual((lo[2],hi[2]),(2690,2825))
        for code in ('MEZ_PRINCIPAL','MEZ_PATAMAR'):
            p=self.refs[code];lo,hi=self.bounds(p)
            self.assertEqual((lo[2],hi[2]),(2825,2850))
            supports=[e for e in self.new if e['tag']!='SOLEIRA_VIDRO' and self.overlap(e,p)[0]>0 and self.overlap(e,p)[1]>0 and self.overlap(e,p)[2]==0]
            self.assertGreater(len(supports),3)

    def test_glass_sills_close_visible_gap_without_material_change(self):
        for glass,sill,base in [('VF08_SUP_ESQ','SG_ESQ','BM_F01'),('VF08_SUP_DIR','SG_DIR','BM_F02')]:
            g=self.refs[glass];s=self.refs[sill];b=self.refs[base]
            lo,hi=self.bounds(s)
            self.assertEqual(lo[1],5596);self.assertEqual(hi[2],2850)
            for x,y,z in g['pontos_mm'][:2]:
                self.assertEqual(z,hi[2]);self.assertTrue(lo[0]<=x<=hi[0] and lo[1]<=y<=hi[1])
            self.assertEqual(self.bounds(b)[1][2],lo[2])
            self.assertEqual(self.bounds(self.refs['MEZ_PRINCIPAL'])[1][1],lo[1])
            old=next(e for e in self.prior['elementos'] if e['id']==glass)
            self.assertEqual(g.get('material_conceitual'),old.get('material_conceitual'))
            self.assertFalse(any(k in g for k in ('material','alpha','opacity','transparencia','cor')))
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['material_fume_aplicado'])
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['extensao_alterada'])

    def test_pitch_and_no_massive_platform(self):
        ts=sorted(e['origem_mm'][1] for e in self.new if e['id'].startswith('BM_T'))
        self.assertEqual(len(ts),13)
        self.assertLessEqual(max(b-a for a,b in zip(ts,ts[1:])),400)
        self.assertFalse(any(e['dimensoes_mm'][0]>=1000 and e['dimensoes_mm'][1]>=1000 for e in self.new))
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['dimensionamento_estrutural'])

    def test_dxf_ascii_r12_contains_geometry(self):
        for view in ('planta','elevacoes'):
            raw=bp.dxf(self.data,view)
            self.assertIn(b'AC1009',raw);self.assertIn(b'\nLINE\n',raw);self.assertTrue(raw.endswith(b'\nEOF\n'))
            for tag in ('OFICINA_REFERENCIA','BASE_MEZ_PRINCIPAL','BASE_MEZ_PATAMAR','BASE_ESQUADRIAS','SOLEIRA_VIDRO','T01_MURO_BC'):
                self.assertIn(tag.encode(),raw)
        plan=bp.dxf(self.data,'planta')
        for code in ('C01','C10','V05','V13'):
            self.assertIn(('\n'+code+'\n').encode(),plan)
        self.assertNotIn(b'\nC09\n',plan)

    def test_collada_valid_xml_and_metric_units(self):
        tree=ET.fromstring(bp.dae(self.data));ns={'c':bp.NS}
        self.assertEqual(tree.find('.//c:unit',ns).attrib['meter'],'0.001')
        self.assertEqual(tree.find('.//c:up_axis',ns).text,'Z_UP')
        self.assertEqual(len(tree.findall('.//c:visual_scene/c:node',ns)),80)
        self.assertEqual(sum(int(x.attrib['count']) for x in tree.findall('.//c:mesh/c:triangles',ns)),640)
        self.assertIsNone(tree.find('.//c:library_materials',ns))

    def test_rejects_missing_units(self):
        self.data['unidades']='m'
        with self.assertRaisesRegex(ValueError,'Schema/unidades'):bp.validate(self.data)

    def test_rejects_nan(self):
        self.refs['PASSE']['pontos_mm'][0][0]=float('nan')
        with self.assertRaises(ValueError):bp.validate(self.data)

    def test_rejects_extra_element_outside_envelope(self):
        self.refs['PASSE']['pontos_mm'][1][0]=10462
        with self.assertRaisesRegex(ValueError,'fora do envelope'):bp.validate(self.data)

    def test_rejects_corrupt_envelope(self):
        self.data['envelope_mm']['z']=6000
        with self.assertRaisesRegex(ValueError,'incoerente'):bp.validate(self.data)

    def test_rejects_duplicate_id(self):
        self.data['elementos'][1]['id']=self.data['elementos'][0]['id']
        with self.assertRaisesRegex(ValueError,'duplicado'):bp.validate(self.data)

    def test_rejects_non_coplanar_face(self):
        self.refs['V09_ENDR']['pontos_mm'][0][0]-=45
        with self.assertRaisesRegex(ValueError,'nao coplanar'):bp.validate(self.data)

    def test_build_manifest_integrity_and_check_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'obra-com-mezanino'/'model.json';path.parent.mkdir();path.write_bytes(EXAMPLE.read_bytes())
            bp.build(path);self.assertTrue(bp.build(path,check=True))
            manifest=json.loads((path.parent/'manifest.json').read_text())
            self.assertEqual(manifest['schema'],bp.SYNC_SCHEMA);self.assertEqual(len(manifest['files']),4)
            for rel,meta in manifest['files'].items():
                content=(path.parent/rel).read_bytes()
                self.assertEqual(meta['sha256'],hashlib.sha256(content).hexdigest());self.assertEqual(meta['size'],len(content))
            (path.parent/'cadcraft/planta.dxf').write_text('TAMPERED')
            with self.assertRaisesRegex(ValueError,'desatualizado'):bp.build(path,check=True)

    def test_deterministic_outputs(self):
        first=(bp.dxf(self.data,'planta'),bp.dxf(self.data,'elevacoes'),bp.dae(self.data))
        second=(bp.dxf(copy.deepcopy(self.data),'planta'),bp.dxf(copy.deepcopy(self.data),'elevacoes'),bp.dae(copy.deepcopy(self.data)))
        self.assertEqual(first,second)

    def test_regenerated_files_match_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'obra-com-mezanino'/'model.json';path.parent.mkdir();path.write_bytes(EXAMPLE.read_bytes())
            bp.build(path);self.assertTrue(bp.build(path,check=True))

if __name__=='__main__':unittest.main()
