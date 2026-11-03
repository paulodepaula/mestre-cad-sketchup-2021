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
        self.prior=json.loads((EXAMPLE.parent/'historico'/'model-R10.json').read_text(encoding='utf-8'))
        self.grid=[e for e in self.refs.values() if e['id'].startswith('G11_')]
        self.sills=[self.refs[k] for k in ('SG_ESQ','SG_DIR')]
        self.prim=[e for e in self.refs.values() if e['tag']=='VIGAS_MEZ_ESTUDO']

    @staticmethod
    def bounds(e):
        lo=e['origem_mm'];return lo,[v+d for v,d in zip(lo,e['dimensoes_mm'])]

    @classmethod
    def overlap(cls,a,b):
        al,ah=cls.bounds(a);bl,bh=cls.bounds(b)
        return [min(ah[j],bh[j])-max(al[j],bl[j]) for j in range(3)]

    @classmethod
    def contact(cls,a,b):
        ds=cls.overlap(a,b)
        return min(ds)>=-1e-6 and sum(d>1e-6 for d in ds)>=2

    def test_r11_contract_and_importer_limits(self):
        self.assertEqual(self.data['revisao'],'R11')
        self.assertEqual(bp.validate(self.data),(10461.,37341.,5600.))
        self.assertEqual(len(self.refs),101)
        self.assertEqual(len(self.grid),47)
        self.assertEqual(sum(e['tipo']=='caixa' for e in self.refs.values()),69)
        self.assertEqual(sum(e['tipo']=='face' for e in self.refs.values()),32)
        self.assertTrue(all(len(e['nome'])<=120 and len(e['tag'])<=40 for e in self.refs.values()))
        self.assertEqual(self.data['parametros_estudo_mm']['implantacao']['oficina'],[4000,6000])

    def test_preserve_every_unrelated_member_from_R10(self):
        self.assertEqual(self.prior['revisao'],'R10')
        self.assertEqual(len(self.prior['elementos']),80)
        oldrefs={e['id']:e for e in self.prior['elementos']}
        removed={k for k in oldrefs if k.startswith(('BM_','BP_'))}
        changed={'MEZ_PRINCIPAL','MEZ_PATAMAR','VF08_SUP_ESQ','VF08_SUP_DIR','SG_ESQ','SG_DIR'}
        self.assertEqual(len(removed),26)
        self.assertEqual(set(self.refs)-set(oldrefs),{e['id'] for e in self.grid})
        self.assertEqual(set(oldrefs)-set(self.refs),removed)
        for code,old in oldrefs.items():
            if code not in removed|changed:self.assertEqual(self.refs[code],old,code)
        for code in ('MEZ_PRINCIPAL','MEZ_PATAMAR','SG_ESQ','SG_DIR'):
            self.assertEqual(self.refs[code]['origem_mm'][:2],oldrefs[code]['origem_mm'][:2])
            self.assertEqual(self.refs[code]['dimensoes_mm'],oldrefs[code]['dimensoes_mm'])
            self.assertEqual(self.refs[code]['origem_mm'][2],oldrefs[code]['origem_mm'][2]-135)
        for code in ('C02','C03','C04','C05','C06'):
            self.assertEqual(self.refs[code]['perfil_referencia']['parede_mm'],3)
        self.assertNotIn('C09',self.refs)
        self.assertEqual(self.data['referencias_estruturais']['aliases_historicos']['C09'],'C04')

    def test_grid_section_inside_frame_and_unknown_wall(self):
        self.assertIsNone(self.data['perfis_estudo']['GRADE_50X50']['parede_mm'])
        self.assertEqual(self.data['perfis_estudo']['GRADE_50X50']['dimensao_externa_mm'],[50,50])
        for e in self.grid:
            lo,hi=self.bounds(e)
            self.assertEqual(sorted(e['dimensoes_mm'])[:2],[50,50])
            self.assertEqual((lo[2],hi[2]),(2640,2690))
            self.assertEqual(e['perfil_ref'],'GRADE_50X50')
            x0,x1,y0,y1=(6561,9361,721,5521) if e['tag']=='GRADE_MEZ_50X50' else (9461,10361,721,2321)
            self.assertTrue(x0<=lo[0]<hi[0]<=x1 and y0<=lo[1]<hi[1]<=y1,e['id'])
        for b in self.prim:self.assertEqual(self.bounds(b)[1][2],2690)
        self.assertFalse(any(e['id'].startswith(('BM_','BP_')) for e in self.refs.values()))

    def test_grid_no_interpenetration_with_itself_columns_or_main_beams(self):
        cols=[e for e in self.refs.values() if e['tipo']=='caixa' and e['id'].startswith('C')]
        new=self.grid+self.sills
        for i,a in enumerate(new):
            for b in new[i+1:]+cols+self.prim:
                self.assertFalse(all(x>1e-6 for x in self.overlap(a,b)),(a['id'],b['id']))

    def test_each_grid_bar_contacts_both_ends(self):
        candidates=self.grid+self.prim
        for a in self.grid:
            axis=0 if a['dimensoes_mm'][0]>50 else 1
            alo,ahi=self.bounds(a)
            for endpoint in (alo[axis],ahi[axis]):
                hits=[]
                for b in candidates:
                    if a['id']==b['id'] or not self.contact(a,b):continue
                    blo,bhi=self.bounds(b)
                    if endpoint in (blo[axis],bhi[axis]):hits.append(b['id'])
                self.assertTrue(hits,(a['id'],endpoint))

    def test_no_floating_grid_or_sill(self):
        reachable={e['id'] for e in self.prim};boxes=self.prim+self.grid+self.sills
        while True:
            found={a['id'] for a in boxes if a['id'] not in reachable and any(b['id'] in reachable and self.contact(a,b) for b in boxes)}
            if not found:break
            reachable.update(found)
        self.assertTrue(all(e['id'] in reachable for e in self.grid+self.sills))

    def test_floor_on_flush_grid_and_135mm_level_change(self):
        for code in ('MEZ_PRINCIPAL','MEZ_PATAMAR'):
            p=self.refs[code];lo,hi=self.bounds(p)
            self.assertEqual((lo[2],hi[2]),(2690,2715))
            supports=[e for e in self.grid if self.overlap(e,p)[0]>0 and self.overlap(e,p)[1]>0 and self.overlap(e,p)[2]==0]
            self.assertGreater(len(supports),3)
        self.assertEqual(self.data['parametros_estudo_mm']['nivel_superior_mezanino'],2715)
        self.assertEqual(self.data['parametros_estudo_mm']['piso_r11']['rebaixamento_mm'],135)
        self.assertEqual(self.refs['MEZ_PRINCIPAL']['dimensoes_mm'],[3000,4975,25])
        self.assertEqual(self.refs['MEZ_PATAMAR']['dimensoes_mm'],[1000,1800,25])

    def test_glass_sill_contact_no_fume_no_top_change(self):
        oldrefs={e['id']:e for e in self.prior['elementos']}
        for glass,sill in [('VF08_SUP_ESQ','SG_ESQ'),('VF08_SUP_DIR','SG_DIR')]:
            g=self.refs[glass];s=self.refs[sill];lo,hi=self.bounds(s)
            self.assertEqual((lo[2],hi[2]),(2690,2715))
            self.assertEqual(lo[1],5596)
            self.assertTrue(self.contact(s,self.refs['V05']))
            for x,y,z in g['pontos_mm'][:2]:
                self.assertEqual(z,hi[2]);self.assertTrue(lo[0]<=x<=hi[0] and lo[1]<=y<=hi[1])
            self.assertEqual(g['pontos_mm'][2:],oldrefs[glass]['pontos_mm'][2:])
            self.assertEqual(g.get('material_conceitual'),oldrefs[glass].get('material_conceitual'))
            self.assertFalse(any(k in g for k in ('material','alpha','opacity','transparencia','cor')))
        self.assertEqual(self.bounds(self.refs['MEZ_PRINCIPAL'])[1][1],self.bounds(self.refs['SG_ESQ'])[0][1])
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['material_fume_aplicado'])
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['extensao_alterada'])

    def test_spacing_segments_and_stair_void(self):
        mt=sorted(e['origem_mm'][1] for e in self.grid if e['id'].startswith('G11_MT'))
        pt=sorted(e['origem_mm'][1] for e in self.grid if e['id'].startswith('G11_PT'))
        self.assertEqual(mt,list(range(971,5372,400)))
        self.assertEqual(pt,[971,1371,1771,2171])
        self.assertEqual(sum(e['id'].startswith('G11_ML') for e in self.grid),26)
        self.assertEqual(sum(e['id'].startswith('G11_PL') for e in self.grid),5)
        for e in self.grid:
            lo,hi=self.bounds(e)
            self.assertFalse(min(hi[0],10361)>max(lo[0],9461) and min(hi[1],6621)>max(lo[1],2421),e['id'])
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['dimensionamento_estrutural'])

    def test_dxf_ascii_r12_contains_geometry(self):
        for view in ('planta','elevacoes'):
            raw=bp.dxf(self.data,view)
            self.assertIn(b'AC1009',raw);self.assertIn(b'\nLINE\n',raw);self.assertTrue(raw.endswith(b'\nEOF\n'))
            for tag in ('OFICINA_REFERENCIA','GRADE_MEZ_50X50','GRADE_PATAMAR_50X50','SOLEIRA_VIDRO','T01_MURO_BC'):
                self.assertIn(tag.encode(),raw)
        plan=bp.dxf(self.data,'planta')
        for code in ('C01','C10','V05','V13'):self.assertIn(('\n'+code+'\n').encode(),plan)
        self.assertNotIn(b'\nC09\n',plan)

    def test_collada_valid_xml_and_metric_units(self):
        tree=ET.fromstring(bp.dae(self.data));ns={'c':bp.NS}
        self.assertEqual(tree.find('.//c:unit',ns).attrib['meter'],'0.001')
        self.assertEqual(tree.find('.//c:up_axis',ns).text,'Z_UP')
        self.assertEqual(len(tree.findall('.//c:visual_scene/c:node',ns)),101)
        self.assertEqual(sum(int(x.attrib['count']) for x in tree.findall('.//c:mesh/c:triangles',ns)),892)
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
