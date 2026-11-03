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
        self.prior=json.loads((EXAMPLE.parent/'historico'/'model-R13.json').read_text(encoding='utf-8'))
        self.oldrefs={e['id']:e for e in self.prior['elementos']}
        self.p=self.data['parametros_estudo_mm']['escada_r14']
        self.grid=[e for e in self.refs.values() if e.get('perfil_ref')=='GRADE_50X50']
        self.prim=[e for e in self.refs.values() if e['tag']=='VIGAS_MEZ_ESTUDO']

    @staticmethod
    def bounds(e):
        if e['tipo']=='caixa':
            lo=e['origem_mm'];return lo,[v+d for v,d in zip(lo,e['dimensoes_mm'])]
        return [[min(p[j] for p in e['pontos_mm']) for j in range(3)], [max(p[j] for p in e['pontos_mm']) for j in range(3)]]

    @classmethod
    def overlap(cls,a,b):
        al,ah=cls.bounds(a);bl,bh=cls.bounds(b)
        return [min(ah[j],bh[j])-max(al[j],bl[j]) for j in range(3)]

    @classmethod
    def contact(cls,a,b):
        ds=cls.overlap(a,b)
        return min(ds)>=-1e-6 and sum(d>1e-6 for d in ds)>=2

    def test_r14_contract(self):
        self.assertEqual(self.data['revisao'],'R14')
        self.assertEqual(bp.validate(self.data),(10461.,37341.,5600.))
        self.assertEqual(len(self.refs),150)
        self.assertEqual(sum(e['tipo']=='caixa' for e in self.refs.values()),89)
        self.assertEqual(sum(e['tipo']=='face' for e in self.refs.values()),61)
        self.assertTrue(all(len(e['nome'])<=120 and len(e['tag'])<=40 for e in self.refs.values()))
        self.assertEqual(self.data['parametros_estudo_mm']['implantacao']['oficina'],[4000,6000])
        self.assertFalse(self.p['conformidade_integral_aprovada'])
        self.assertFalse(self.p['escada_executiva_dimensionada'])

    def test_geometry_matches_checked_coordinates(self):
        rows=[]
        for e in sorted(self.refs.values(),key=lambda x:x['id']):
            pts=e['pontos_mm'] if e['tipo']=='face' else [e['origem_mm'],e['dimensoes_mm']]
            rows.append([e['id'],e['tipo'],e['tag'],[[float(x) for x in p] for p in pts]])
        digest=hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()
        self.assertEqual(digest,'ae66dc2532749f6f9c12abf27c7e4e3a703768bff02a7ed5412c5286ab78fb12')

    def test_only_listed_original_elements_change(self):
        self.assertEqual(self.prior['revisao'],'R13')
        self.assertEqual(len(self.oldrefs),101)
        expected_changed={'ESCADA_RES','MEZ_PRINCIPAL','V03','G11_ML01_05','G11_ML02_05'}|{'G11_MT%02d'%i for i in range(5,13)}
        expected_removed={'G11_ML02_%02d'%i for i in range(6,14)}
        self.assertEqual(set(self.p['alteracoes_existentes']),expected_changed)
        self.assertEqual(set(self.p['retirados']),expected_removed)
        self.assertEqual(set(self.oldrefs)-set(self.refs),expected_removed)
        self.assertEqual(len(set(self.refs)-set(self.oldrefs)),57)
        for code,old in self.oldrefs.items():
            if code not in expected_changed|expected_removed:self.assertEqual(self.refs[code],old,code)
        for key in ('levantamento_campo_mm','levantamento_terreno','perfis_estudo','envelope_mm'):
            self.assertEqual(self.data[key],self.prior[key],key)

    def test_columns_roof_glass_preserved(self):
        for k,e in self.oldrefs.items():
            if k.startswith('C') or e['tag'] in ('VIGAS_COB_ESTUDO','TRAVESSAS_BALANCO_ESTUDO','VIDRO_FUNDOS_ESTUDO','SOLEIRA_VIDRO','T01_TERRENO','T01_MURO_BC'):
                self.assertEqual(self.refs[k],e,k)
        self.assertEqual(self.refs['C02']['dimensoes_mm'],[100,100,5420])
        self.assertEqual(self.refs['C02']['perfil_referencia']['parede_mm'],3)
        self.assertNotIn('C09',self.refs)
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['extensao_alterada'])
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['material_fume_aplicado'])

    def test_step_count_and_rise_uniformity(self):
        ds=[e for e in self.refs.values() if e['tag']=='ESCADA_DEGRAUS']
        rs=[e for e in self.refs.values() if e['tag']=='ESCADA_ESPELHOS']
        self.assertEqual(len(ds),14);self.assertEqual(len(rs),16)
        h=2715/16
        self.assertEqual(self.p['espelho_mm'],h)
        self.assertTrue(160<=h<=180)
        self.assertTrue(630<=2*h+300<=640)
        self.assertEqual(self.bounds(self.refs['E14_PAT'])[1][2],8*h)
        for k in range(1,17):
            lo,hi=self.bounds(self.refs['E14_R%02d'%k])
            self.assertAlmostEqual(lo[2],(k-1)*h);self.assertAlmostEqual(hi[2],k*h)
        for k in list(range(1,8))+list(range(9,16)):
            e=self.refs['E14_D%02d'%k];lo,hi=self.bounds(e)
            self.assertEqual(e['dimensoes_mm'],[900,300,30])
            self.assertEqual(hi[2],k*h)

    def test_position_and_arrival_no_forward_overhang(self):
        stair=[e for e in self.refs.values() if e['id'].startswith('E14_')]
        self.assertEqual(len(stair),52)
        for e in stair:
            lo,hi=self.bounds(e)
            self.assertTrue(8261<=lo[0]<=hi[0]<=10361,e['id'])
            self.assertTrue(2421<=lo[1]<=hi[1]<=5521,e['id'])
            self.assertLessEqual(hi[1],self.refs['C07']['origem_mm'][1])
        self.assertEqual(self.bounds(self.refs['MEZ_PATAMAR'])[1][1],2421)
        self.assertEqual(self.refs['E14_R16']['pontos_mm'][0][1],2421)
        self.assertEqual(self.bounds(self.refs['E14_R16'])[1][2],2715)
        self.assertEqual(self.data['parametros_estudo_mm']['nivel_superior_mezanino'],2715)

    def test_landing_size_and_clear_widths(self):
        self.assertEqual(self.refs['E14_PAT']['dimensoes_mm'],[2100,1000,25])
        self.assertEqual(self.p['largura_entre_faces_longarinas_mm'],900)
        self.assertEqual(self.refs['E14_L02']['pontos_mm'][0][0]-self.refs['E14_L01']['pontos_mm'][0][0],900)
        self.assertEqual(self.refs['E14_L04']['pontos_mm'][0][0]-self.refs['E14_L03']['pontos_mm'][0][0],900)
        self.assertEqual(self.refs['E14_L03']['pontos_mm'][0][0]-self.refs['E14_L02']['pontos_mm'][0][0],200)

    def test_new_boxes_do_not_penetrate_other_boxes(self):
        boxes=[e for e in self.refs.values() if e['tipo']=='caixa']
        for a in boxes:
            if a['id'] in self.oldrefs:continue
            for b in boxes:
                if a['id']==b['id']:continue
                self.assertFalse(all(v>1e-6 for v in self.overlap(a,b)),(a['id'],b['id']))

    def test_four_intermediate_platform_supports(self):
        beams=[self.refs['E14_B%02d'%i] for i in range(1,5)]
        posts=[self.refs['E14_P%02d'%i] for i in range(1,5)]
        deck=self.refs['E14_PAT']
        for post in posts:
            self.assertEqual(post['origem_mm'][2],0)
            self.assertTrue(any(self.contact(post,b) for b in beams))
        for b in beams:self.assertTrue(self.contact(b,deck))

    def test_stairwell_header_contacts_existing_beams(self):
        self.assertEqual(self.refs['V03']['dimensoes_mm'],[100,1800,180])
        self.assertEqual(self.refs['V14']['origem_mm'],[8161,2421,2510])
        self.assertEqual(self.refs['V15']['origem_mm'],[6561,2321,2510])
        for a,b in [('V15','V03'),('V15','V04'),('V14','V15'),('V14','V05')]:
            self.assertTrue(self.contact(self.refs[a],self.refs[b]),(a,b))

    def test_grid_stays_inside_beams_and_has_contact(self):
        self.assertEqual(len(self.grid),40)
        self.assertIsNone(self.data['perfis_estudo']['GRADE_50X50']['parede_mm'])
        allbars=self.grid+self.prim
        cols=[e for e in self.refs.values() if e['tipo']=='caixa' and e['id'].startswith('C')]
        for a in self.grid:
            lo,hi=self.bounds(a)
            self.assertEqual(sorted(a['dimensoes_mm'])[:2],[50,50])
            self.assertEqual((lo[2],hi[2]),(2640,2690))
            for b in allbars+cols:
                if a['id']!=b['id']:self.assertFalse(all(x>1e-6 for x in self.overlap(a,b)),(a['id'],b['id']))
            axis=0 if a['dimensoes_mm'][0]>50 else 1
            for end in (lo[axis],hi[axis]):
                hits=[b for b in allbars if a['id']!=b['id'] and self.contact(a,b) and end in (self.bounds(b)[0][axis],self.bounds(b)[1][axis])]
                self.assertTrue(hits,(a['id'],end))

    def test_floor_area_loss_explicit_and_no_overhead_slab(self):
        floors=[e for e in self.refs.values() if e['tag']=='MEZANINO_ESTUDO']
        old=[e for e in self.oldrefs.values() if e['tag']=='MEZANINO_ESTUDO']
        area=lambda xs:sum(e['dimensoes_mm'][0]*e['dimensoes_mm'][1] for e in xs)/1e6
        self.assertAlmostEqual(area(old),16.725)
        self.assertAlmostEqual(area(floors),12.9975)
        self.assertAlmostEqual(area(old)-area(floors),self.p['area_retirada_mezanino_m2'])
        for e in floors:
            lo,hi=self.bounds(e);self.assertEqual((lo[2],hi[2]),(2690,2715))
            self.assertFalse(min(hi[0],10361)>max(lo[0],8261) and min(hi[1],5521)>max(lo[1],2421),e['id'])

    def test_sampled_headroom_at_steps_and_landing(self):
        boxes=[e for e in self.refs.values() if e['tipo']=='caixa']
        for step in [e for e in boxes if e['tag']=='ESCADA_DEGRAUS' or e['id']=='E14_PAT']:
            lo,hi=self.bounds(step)
            for fx in (.1,.5,.9):
                for fy in (.1,.5,.9):
                    x=lo[0]+fx*(hi[0]-lo[0]);y=lo[1]+fy*(hi[1]-lo[1]);z=hi[2]
                    limits=[5350+(x-5461)*.05-z]
                    for b in boxes:
                        bl,bh=self.bounds(b)
                        if b['id']!=step['id'] and bl[0]<x<bh[0] and bl[1]<y<bh[1] and bl[2]>=z:limits.append(bl[2]-z)
                    for k in ('V07','V08','V09','V13'):
                        bl,bh=self.bounds(self.refs[k+'_BOTTOM'])
                        if bl[0]<=x<=bh[0] and bl[1]<=y<=bh[1]:limits.append(5160+(x-5461)*.05-z)
                    self.assertGreaterEqual(min(limits),2100,(step['id'],x,y,min(limits)))

    def test_guard_and_stringer_planes_are_not_execution_specs(self):
        self.assertEqual(sum(e['tag']=='ESCADA_GUARDAS' for e in self.refs.values()),9)
        self.assertEqual(sum(e['tag']=='ESCADA_LONGARINAS' for e in self.refs.values()),4)
        for i in range(1,5):
            e=self.refs['E14_L%02d'%i]
            self.assertEqual(e['tipo'],'face');self.assertIsNone(e['espessura_chapa_mm'])
        self.assertIsNone(self.p['espessura_aco_degraus_mm'])

    def test_dxf_and_collada(self):
        for view in ('planta','elevacoes'):
            raw=bp.dxf(self.data,view)
            self.assertIn(b'AC1009',raw);self.assertTrue(raw.endswith(b'\nEOF\n'))
            for tag in ('ESCADA_DEGRAUS','ESCADA_PATAMAR','ESCADA_ESPELHOS','ESCADA_LONGARINAS','ESCADA_GUARDAS','T01_MURO_BC'):
                self.assertIn(tag.encode(),raw)
        tree=ET.fromstring(bp.dae(self.data));ns={'c':bp.NS}
        self.assertEqual(tree.find('.//c:unit',ns).attrib['meter'],'0.001')
        self.assertEqual(tree.find('.//c:up_axis',ns).text,'Z_UP')
        self.assertEqual(len(tree.findall('.//c:visual_scene/c:node',ns)),150)
        self.assertEqual(sum(int(x.attrib['count']) for x in tree.findall('.//c:mesh/c:triangles',ns)),1190)
        self.assertIsNone(tree.find('.//c:library_materials',ns))

    def test_rejects_bad_units_nan_duplicate_and_bad_envelope(self):
        variants=[]
        d=copy.deepcopy(self.data);d['unidades']='m';variants.append(d)
        d=copy.deepcopy(self.data);d['elementos'][0]['pontos_mm'][0][0]=float('nan');variants.append(d)
        d=copy.deepcopy(self.data);d['elementos'][1]['id']=d['elementos'][0]['id'];variants.append(d)
        d=copy.deepcopy(self.data);d['envelope_mm']['z']=6000;variants.append(d)
        d=copy.deepcopy(self.data);d['elementos'][0]['pontos_mm'][0][0]=10462;variants.append(d)
        for d in variants:
            with self.assertRaises(ValueError):bp.validate(d)

    def test_rejects_non_coplanar_and_unsupported_geometry(self):
        d=copy.deepcopy(self.data);next(e for e in d['elementos'] if e['id']=='V09_ENDR')['pontos_mm'][0][0]-=45
        with self.assertRaises(ValueError):bp.validate(d)
        d=copy.deepcopy(self.data);d['elementos'][0]['tipo']='ruby_exec'
        with self.assertRaises(ValueError):bp.validate(d)

    def test_deterministic_outputs_and_manifest_integrity(self):
        self.assertEqual(bp.dae(self.data),bp.dae(copy.deepcopy(self.data)))
        self.assertEqual(bp.dxf(self.data,'planta'),bp.dxf(copy.deepcopy(self.data),'planta'))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'obra-com-mezanino'/'model.json';path.parent.mkdir();path.write_bytes(EXAMPLE.read_bytes())
            bp.build(path);self.assertTrue(bp.build(path,check=True))
            manifest=json.loads((path.parent/'manifest.json').read_text())
            self.assertEqual(manifest['revisao'],'R14')
            for rel,meta in manifest['files'].items():
                b=(path.parent/rel).read_bytes();self.assertEqual(meta['sha256'],hashlib.sha256(b).hexdigest());self.assertEqual(meta['size'],len(b))
            (path.parent/'cadcraft/planta.dxf').write_text('TAMPERED')
            with self.assertRaises(ValueError):bp.build(path,check=True)

if __name__=='__main__':unittest.main()
