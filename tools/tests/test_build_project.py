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
        self.prior=json.loads((EXAMPLE.parent/'historico'/'model-R12.json').read_text(encoding='utf-8'))
        self.oldrefs={e['id']:e for e in self.prior['elementos']}
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

    def test_r13_contract_and_importer_limits(self):
        self.assertEqual(self.data['revisao'],'R13')
        self.assertEqual(bp.validate(self.data),(10461.,37341.,5600.))
        self.assertEqual(len(self.refs),101)
        self.assertEqual(len(self.grid),47)
        self.assertEqual(sum(e['tipo']=='caixa' for e in self.refs.values()),69)
        self.assertEqual(sum(e['tipo']=='face' for e in self.refs.values()),32)
        self.assertTrue(all(len(e['nome'])<=120 and len(e['tag'])<=40 for e in self.refs.values()))
        self.assertEqual(self.data['parametros_estudo_mm']['implantacao']['oficina'],[4000,6000])

    def test_r13_changes_only_C02_and_preserves_other_100_elements(self):
        self.assertEqual(self.prior['revisao'],'R12')
        self.assertEqual(len(self.oldrefs),101)
        self.assertEqual(list(self.refs),list(self.oldrefs))
        changed=[key for key in self.oldrefs if self.oldrefs[key]!=self.refs[key]]
        self.assertEqual(changed,['C02'])
        self.assertEqual(self.data['levantamento_campo_mm'],self.prior['levantamento_campo_mm'])
        self.assertEqual(self.data['levantamento_terreno'],self.prior['levantamento_terreno'])
        self.assertEqual(self.data['perfis_estudo'],self.prior['perfis_estudo'])
        self.assertEqual(self.data['envelope_mm'],self.prior['envelope_mm'])
        for key,value in self.prior['parametros_estudo_mm'].items():
            if key not in ('pilares_r07','escada_r12'):
                self.assertEqual(value,self.data['parametros_estudo_mm'][key],key)
        for key,value in self.prior['referencias_estruturais'].items():
            if key!='revisao':self.assertEqual(value,self.data['referencias_estruturais'][key],key)
        self.assertEqual(self.data['historico']['base'],'R12')
        for key in ('C03','C04','C05','C06'):
            self.assertEqual(self.refs[key]['dimensoes_mm'][:2],[150,150])
            self.assertEqual(self.refs[key]['perfil_referencia']['parede_mm'],3)
        self.assertNotIn('C09',self.refs)

    def test_C02_100x100x3_keeps_height_and_outside_face(self):
        c=self.refs['C02'];old=self.oldrefs['C02']
        self.assertEqual(c['origem_mm'],[10361,3571,0])
        self.assertEqual(c['dimensoes_mm'],[100,100,5420])
        self.assertEqual(old['dimensoes_mm'],[150,150,5420])
        self.assertEqual(c['perfil_referencia']['dimensao_externa_mm'],[100,100])
        self.assertEqual(c['perfil_referencia']['parede_mm'],3)
        self.assertEqual(self.bounds(c)[1][0],self.bounds(old)[1][0])
        self.assertEqual(self.bounds(c)[1][0],10461)
        self.assertEqual(c['origem_mm'][1:],old['origem_mm'][1:])
        self.assertEqual(c['tag'],old['tag'])
        self.assertEqual(c['tipo'],old['tipo'])

    def test_C02_stair_intrusion_removed_not_stair_dimension_certification(self):
        points=self.refs['ESCADA_RES']['pontos_mm']
        sx0=min(p[0] for p in points);sx1=max(p[0] for p in points)
        sy0=min(p[1] for p in points);sy1=max(p[1] for p in points)
        lo,hi=self.bounds(self.refs['C02'])
        intrusion=max(0,min(sx1,hi[0])-max(sx0,lo[0]))
        overlap_y=min(sy1,hi[1])-max(sy0,lo[1])
        self.assertEqual((intrusion,overlap_y),(0,100))
        self.assertEqual(sx1-sx0-intrusion,900)
        oldlo,oldhi=self.bounds(self.oldrefs['C02'])
        self.assertEqual(min(sx1,oldhi[0])-max(sx0,oldlo[0]),50)
        note=self.data['parametros_estudo_mm']['escada_r12']['interferencia_preexistente_C02']
        self.assertEqual(note['invasao_lateral_mm'],0)
        self.assertEqual(note['largura_restante_nominal_mm'],900)
        self.assertTrue(note['resolvida'])
        self.assertEqual(note['revisao_resolucao'],'R13')
        self.assertFalse(self.data['parametros_estudo_mm']['escada_r12']['escada_executiva_dimensionada'])

    def test_C02_contact_V01_and_encounter_V10_does_not_imply_zero_load(self):
        c=self.refs['C02']
        self.assertEqual(self.overlap(c,self.refs['V01']),[100,100,0])
        self.assertEqual(self.overlap(c,self.refs['V10']),[100,100,180])
        self.assertTrue(self.contact(c,self.refs['V01']))
        params=self.data['parametros_estudo_mm']['coluna_C02_r13']
        self.assertFalse(params['cargas_nulas_confirmadas'])
        self.assertFalse(params['dimensionamento_estrutural'])
        self.assertIn('V01 - cobertura',params['encontros_geometricos'])
        self.assertIn('V10 - mezanino',params['encontros_geometricos'])
        self.assertIn('NAO',c['nota_cargas'])

    def test_stair_still_stops_at_C07_face_and_keeps_landing(self):
        e=self.refs['ESCADA_RES'];c=self.refs['C07'];c10=self.refs['C10'];p=self.refs['MEZ_PATAMAR']
        self.assertEqual(e,self.oldrefs['ESCADA_RES'])
        self.assertEqual(e['pontos_mm'],[[10361,5621,0],[9461,5621,0],[9461,2421,0],[10361,2421,0]])
        xs=[v[0] for v in e['pontos_mm']];ys=[v[1] for v in e['pontos_mm']]
        self.assertEqual(max(ys),c['origem_mm'][1]+c['dimensoes_mm'][1])
        self.assertEqual(max(ys),c10['origem_mm'][1]+c10['dimensoes_mm'][1])
        self.assertEqual(max(ys),self.refs['VF08_SUP_DIR']['pontos_mm'][0][1])
        self.assertEqual(min(ys),p['origem_mm'][1]+p['dimensoes_mm'][1])
        self.assertEqual((max(xs)-min(xs),max(ys)-min(ys)),(900,3200))
        self.assertEqual(e['nivel_chegada_mm'],p['origem_mm'][2]+p['dimensoes_mm'][2])
        self.assertEqual(e['nivel_chegada_mm'],2715)
        self.assertIsNone(self.data['parametros_estudo_mm']['escada_r12']['geometria_dos_degraus'])

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
        for glass,sill in [('VF08_SUP_ESQ','SG_ESQ'),('VF08_SUP_DIR','SG_DIR')]:
            g=self.refs[glass];s=self.refs[sill];lo,hi=self.bounds(s)
            self.assertEqual((lo[2],hi[2]),(2690,2715))
            self.assertEqual(lo[1],5596)
            self.assertTrue(self.contact(s,self.refs['V05']))
            for x,y,z in g['pontos_mm'][:2]:
                self.assertEqual(z,hi[2]);self.assertTrue(lo[0]<=x<=hi[0] and lo[1]<=y<=hi[1])
            self.assertEqual(g,self.oldrefs[glass])
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
            self.assertFalse(min(hi[0],10361)>max(lo[0],9461) and min(hi[1],5621)>max(lo[1],2421),e['id'])
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['dimensionamento_estrutural'])

    def test_dxf_ascii_r12_contains_geometry(self):
        for view in ('planta','elevacoes'):
            raw=bp.dxf(self.data,view)
            self.assertIn(b'AC1009',raw);self.assertIn(b'\nLINE\n',raw);self.assertTrue(raw.endswith(b'\nEOF\n'))
            for tag in ('OFICINA_REFERENCIA','GRADE_MEZ_50X50','GRADE_PATAMAR_50X50','SOLEIRA_VIDRO','T01_MURO_BC','ESCADA_HIPOTESE'):
                self.assertIn(tag.encode(),raw)
        plan=bp.dxf(self.data,'planta')
        for code in ('C01','C02','C10','V05','V13'):self.assertIn(('\n'+code+'\n').encode(),plan)
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
