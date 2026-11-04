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
        self.r13=json.loads((EXAMPLE.parent/'historico'/'model-R13.json').read_text(encoding='utf-8'))
        self.r14=json.loads((EXAMPLE.parent/'historico'/'model-R14.json').read_text(encoding='utf-8'))
        self.r15=json.loads((EXAMPLE.parent/'historico'/'model-R15.json').read_text(encoding='utf-8'))
        self.p=self.data['parametros_estudo_mm']['escada_r15']

    @staticmethod
    def bounds(e):
        if e['tipo']=='caixa':
            lo=e['origem_mm']; return lo,[v+d for v,d in zip(lo,e['dimensoes_mm'])]
        return [[min(p[j] for p in e['pontos_mm']) for j in range(3)],
                [max(p[j] for p in e['pontos_mm']) for j in range(3)]]

    @classmethod
    def overlap(cls,a,b):
        al,ah=cls.bounds(a); bl,bh=cls.bounds(b)
        return [min(ah[j],bh[j])-max(al[j],bl[j]) for j in range(3)]

    def test_r15_contract(self):
        self.assertEqual(self.data['revisao'],'R24')
        self.assertEqual(bp.validate(self.data),(10461.,37341.,5600.))
        self.assertEqual(len(self.refs),230)
        self.assertEqual(sum(e['tipo']=='caixa' for e in self.refs.values()),126)
        self.assertEqual(sum(e['tipo']=='face' for e in self.refs.values()),104)
        self.assertEqual(self.data['parametros_estudo_mm']['implantacao']['oficina'],[4000,6000])
        self.assertFalse(self.p['escada_executiva_dimensionada'])
        self.assertFalse(self.p['conformidade_integral_aprovada'])

    def test_r14_u_removed_and_r13_structure_recovered(self):
        for code in ('V14','V15','MEZ_FRENTE_R14','MEZ_FAIXA_R14','G14_ML01_CONT'):
            self.assertNotIn(code,self.refs)
        self.assertFalse(any(k.startswith('E14_') for k in self.refs))
        self.assertEqual(self.refs['MEZ_PRINCIPAL'],next(e for e in self.r13['elementos'] if e['id']=='MEZ_PRINCIPAL'))
        self.assertEqual(self.refs['V03'],next(e for e in self.r13['elementos'] if e['id']=='V03'))
        self.assertEqual(self.refs['C02'],next(e for e in self.r13['elementos'] if e['id']=='C02'))

    def test_only_local_R13_items_changed_or_removed(self):
        old={e['id']:e for e in self.r13['elementos']}
        changed={'ESCADA_RES','MEZ_PATAMAR','V11','G11_PL01_03','COB_R03'}
        removed={'G11_PT03','G11_PT04','G11_PL01_04','G11_PL01_05'}
        added={k for k in self.refs if k not in old}
        self.assertEqual(len(added),133)
        self.assertTrue(all(k.startswith('E24_') or k.startswith('MAD17_') or k.startswith('P18_') or k.startswith('P21_') or k.startswith('PV23_') for k in added))
        self.assertEqual(set(old)-set(self.refs),removed)
        for k,e in old.items():
            if k not in changed|removed:
                self.assertEqual(self.refs[k],e,k)

    def test_r24_compact_L_stair_dimensions(self):
        p=self.data['parametros_estudo_mm']['escada_r24']
        self.assertEqual(p['numero_espelhos'],15)
        self.assertEqual(p['espelho_mm'],181)
        self.assertEqual(p['numero_pisos_total'],14)
        self.assertEqual(p['largura_nominal_mm'],900)
        self.assertEqual(p['trecho_inferior']['quantidade_pisos'],3)
        self.assertEqual(p['trecho_inferior']['desenvolvimento_mm'],999)
        self.assertEqual(p['trecho_inferior']['pisada_mm'],333)
        self.assertEqual(p['lance_principal']['quantidade_pisos'],11)
        self.assertEqual(p['lance_principal']['desenvolvimento_mm'],3058)
        self.assertEqual(p['lance_principal']['pisada_mm'],278)
        self.assertEqual(p['faixa_livre_junto_porta_mm']['profundidade'],834)
        self.assertEqual(p['nivel_chegada_mm'],2715)
        self.assertFalse(p['escada_executiva_dimensionada'])

    def test_r24_lower_leg_and_main_flight_geometry(self):
        low=[self.refs['E24_LD%02d'%i] for i in range(1,4)]
        main=[self.refs['E24_MD%02d'%i] for i in range(1,12)]
        self.assertEqual([e['dimensoes_mm'] for e in low],[[333,900,30]]*3)
        self.assertEqual([e['origem_mm'][0] for e in low],[8462,8795,9128])
        self.assertEqual([e['dimensoes_mm'] for e in main],[[900,278,30]]*11)
        self.assertEqual(main[-1]['origem_mm'][1],1629)
        self.assertEqual(main[-1]['origem_mm'][2]+30,2534)
        self.assertEqual(self.refs['E24_MR12']['pontos_mm'][-1][2],2715)
        self.assertEqual(self.refs['E24_CANTO']['dimensoes_mm'],[300,900,30])

    def test_r24_keeps_door_access_zone_free_of_treads(self):
        door_zone={'tipo':'caixa','origem_mm':[9461,4687,0],'dimensoes_mm':[900,834,2000]}
        treads=[e for e in self.refs.values() if e['tag']=='ESCADA_DEGRAUS']
        for e in treads:
            self.assertFalse(all(v>1e-6 for v in self.overlap(e,door_zone)),e['id'])
        for code in ('C07','C10'):
            c=self.refs[code]
            for e in treads:
                self.assertFalse(all(v>1e-6 for v in self.overlap(e,c)),(e['id'],code))

    def test_r24_upper_landing_and_structure_preserved(self):
        self.assertEqual(self.refs['MEZ_PATAMAR']['origem_mm'],[9461,621,2690])
        self.assertEqual(self.refs['MEZ_PATAMAR']['dimensoes_mm'],[1000,1008,25])
        self.assertEqual(self.refs['V11']['origem_mm'],[9461,1529,2510])
        self.assertEqual(self.refs['V11']['dimensoes_mm'],[1000,100,180])
        for code in ('E24_ML01','E24_ML02','E24_G01'):
            self.assertEqual(self.refs[code]['tipo'],'face')
        self.assertIsNone(self.refs['E24_ML01']['espessura_chapa_mm'])
        self.assertEqual(self.refs['E24_G01']['altura_referencia_mm'],1100)

    def test_preserves_roof_glass_and_terrain_from_R13(self):
        old={e['id']:e for e in self.r13['elementos']}
        for k in ('VF08_SUP_ESQ','VF08_SUP_DIR','T01_TERRENO','MURO_BC','V05','V13_TOP','C04','C07','C10'):
            self.assertEqual(self.refs[k],old[k],k)
        self.assertEqual(self.refs['COB_R03']['pontos_mm'],old['COB_R03']['pontos_mm'])
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['material_fume_aplicado'])
        self.assertFalse(self.data['parametros_estudo_mm']['escopo']['telhado_alterado'])

    def test_r16_wood_panel_and_sandwich_roof_finish(self):
        slats=[e for e in self.refs.values() if e['tag']=='PAINEL_MADEIRA_INTERNO']
        self.assertEqual(len(slats),18)
        self.assertEqual(slats[0]['origem_mm'],[10341,5621,0])
        self.assertEqual(slats[0]['dimensoes_mm'],[20,900,294])
        self.assertEqual(slats[-1]['origem_mm'],[10341,5621,5253])
        self.assertEqual(slats[-1]['dimensoes_mm'],[20,900,341])
        self.assertEqual(max(e['origem_mm'][2]+e['dimensoes_mm'][2] for e in slats),5594)
        self.assertTrue(all(e['material_conceitual']=='MADEIRA_AMADEIRADA_TOM_QUENTE' for e in slats))
        stair=[e for e in self.refs.values() if e['id'].startswith('E24_')]
        for s in slats:
            for e in stair:
                self.assertFalse(all(v>1e-6 for v in self.overlap(s,e)),(s['id'],e['id']))
        roof=self.refs['COB_R03']
        oldroof=next(e for e in self.r15['elementos'] if e['id']=='COB_R03')
        self.assertEqual(roof['pontos_mm'],oldroof['pontos_mm'])
        self.assertEqual(roof['material_conceitual'],'TELHA_SANDUICHE_AMADEIRADA')
        self.assertEqual(roof['acabamento_inferior'],'AMADEIRADO')
        self.assertTrue(roof['geometria_R15_preservada'])

    def test_r17_wood_panel_fits_exactly_between_C10_and_C01(self):
        slats=[e for e in self.refs.values() if e['tag']=='PAINEL_MADEIRA_INTERNO']
        c10=self.refs['C10']; c01=self.refs['C01']
        y0=c10['origem_mm'][1]+c10['dimensoes_mm'][1]
        y1=c01['origem_mm'][1]
        self.assertEqual((y0,y1,y1-y0),(5621,6521,900))
        self.assertEqual(len(slats),18)
        for s in slats:
            self.assertEqual(s['origem_mm'][0],10341)
            self.assertEqual(s['origem_mm'][1],5621)
            self.assertEqual(s['dimensoes_mm'][0:2],[20,900])
            self.assertEqual(s['origem_mm'][1]+s['dimensoes_mm'][1],6521)
            for c in (c10,c01):
                self.assertFalse(all(v>1e-6 for v in self.overlap(s,c)),(s['id'],c['id']))
        self.assertEqual(max(s['origem_mm'][2]+s['dimensoes_mm'][2] for s in slats),5594)
        stair=[e for e in self.refs.values() if e['id'].startswith('E24_')]
        for s in slats:
            for e in stair:
                self.assertFalse(all(v>1e-6 for v in self.overlap(s,e)),(s['id'],e['id']))

    def test_r18_rolling_grille_between_C04_and_C07(self):
        c04=self.refs['C04']; c07=self.refs['C07']; v05=self.refs['V05']
        x0=c04['origem_mm'][0]+c04['dimensoes_mm'][0]
        x1=c07['origem_mm'][0]
        self.assertEqual((x0,x1,x1-x0),(6611,9361,2750))
        self.assertEqual(v05['origem_mm'][2],2510)
        self.assertNotIn('P18_FOLHA',self.refs)
        g1=self.refs['P18_GUIA_C04']; g2=self.refs['P18_GUIA_C07']
        self.assertEqual(g1['origem_mm'],[6611,5561,0])
        self.assertEqual(g1['dimensoes_mm'],[40,60,2510])
        self.assertEqual(g2['origem_mm'],[9321,5561,0])
        self.assertEqual(g2['dimensoes_mm'],[40,60,2510])
        # Guias ficam no vao livre e apenas encostam nas faces internas das colunas.
        for g,c in ((g1,c04),(g2,c07)):
            self.assertFalse(all(v>1e-6 for v in self.overlap(g,c)),(g['id'],c['id']))
        p=self.data['parametros_estudo_mm']['porta_enrolar_r18']
        self.assertEqual(p['vao_bruto_mm']['largura'],2750)
        self.assertEqual(p['vao_bruto_mm']['altura_ate_v05'],2510)
        self.assertFalse(p['estrutural'])

    def test_r21_rolling_door_uses_horizontal_microperforated_slats(self):
        slats=[e for e in self.refs.values() if e['id'].startswith('P21_L')]
        self.assertEqual(len(slats),25)
        self.assertTrue(all(e['tag']=='PORTA_ENROLAR_MICROPERF' for e in slats))
        self.assertTrue(all(e['dimensoes_mm']==[2750,20,78] for e in slats))
        self.assertEqual([e['origem_mm'][2] for e in slats],list(range(0,2161,90)))
        self.assertFalse(any(e['id'].startswith('P20_') for e in self.refs.values()))
        box=self.refs['P21_CAIXA_SUP']
        self.assertEqual(box['origem_mm'],[6611,5481,2310])
        self.assertEqual(box['dimensoes_mm'],[2750,140,200])
        p=self.data['parametros_estudo_mm']['porta_enrolar_r21']
        self.assertEqual(p['tipo'],'porta metalica de enrolar com laminas horizontais microperfuradas')
        self.assertEqual(p['laminas']['quantidade'],25)
        self.assertFalse(p['executivo'])

    def test_r23_solar_modules_have_frame_surface_and_rails(self):
        glass=[e for e in self.refs.values() if e['id'].startswith('PV23_') and e['id'].endswith('_GLASS')]
        frames=[e for e in self.refs.values() if e['id'].startswith('PV23_') and any(e['id'].endswith('_F%d'%i) for i in range(1,5))]
        rails=[e for e in self.refs.values() if e['id'].startswith('PV23_RAIL_')]
        self.assertEqual(len(glass),10)
        self.assertEqual(len(frames),40)
        self.assertEqual(len(rails),4)
        self.assertFalse(any(e['id'].startswith('SOL22_') for e in self.refs.values()))
        # Cada conjunto preserva envelope externo 2278 x 1134 mm.
        for n in range(1,11):
            parts=[self.refs['PV23_%02d_GLASS'%n]]+[self.refs['PV23_%02d_F%d'%(n,i)] for i in range(1,5)]
            xs=[p[0] for e in parts for p in e['pontos_mm']]
            ys=[p[1] for e in parts for p in e['pontos_mm']]
            # Comprimento real inclinado entre os extremos da moldura.
            pts=[]
            for e in parts: pts+=e['pontos_mm']
            # extremos em y minimo; distancia 3D no sentido do caimento
            ymin=min(ys)
            edge=[p for p in pts if abs(p[1]-ymin)<0.01]
            lo=min(edge,key=lambda p:p[0]); hi=max(edge,key=lambda p:p[0])
            dist=sum((lo[i]-hi[i])**2 for i in range(3))**0.5
            self.assertAlmostEqual(dist,2278,places=2)
            self.assertAlmostEqual(max(ys)-min(ys),1134,places=2)
        p=self.data['parametros_estudo_mm']['solar_r23']
        self.assertEqual(p['quantidade'],10)
        self.assertEqual(p['detalhamento']['trilhos_apoio'],4)
        self.assertEqual(p['modulo_externo_mm'],{'comprimento':2278,'largura':1134,'espessura':30})
        self.assertFalse(p['executivo'])

    def test_dxf_and_collada(self):
        for view in ('planta','elevacoes'):
            raw=bp.dxf(self.data,view)
            self.assertIn(b'AC1009',raw); self.assertTrue(raw.endswith(b'\nEOF\n'))
            for tag in ('ESCADA_DEGRAUS','ESCADA_ESPELHOS','ESCADA_LONGARINAS','ESCADA_GUARDAS','T01_MURO_BC','PORTA_ENROLAR_MICROPERF','PAINEL_SOLAR_CELULAS','PAINEL_SOLAR_MOLDURA','PAINEL_SOLAR_TRILHOS'):
                self.assertIn(tag.encode(),raw)
        tree=ET.fromstring(bp.dae(self.data)); ns={'c':bp.NS}
        self.assertEqual(tree.find('.//c:unit',ns).attrib['meter'],'0.001')
        self.assertEqual(tree.find('.//c:up_axis',ns).text,'Z_UP')
        self.assertEqual(len(tree.findall('.//c:visual_scene/c:node',ns)),230)
        self.assertEqual(sum(int(x.attrib['count']) for x in tree.findall('.//c:mesh/c:triangles',ns)),1720)

    def test_rejects_invalid_geometry(self):
        d=copy.deepcopy(self.data); d['unidades']='m'
        with self.assertRaises(ValueError): bp.validate(d)
        d=copy.deepcopy(self.data); d['elementos'][0]['id']=d['elementos'][1]['id']
        with self.assertRaises(ValueError): bp.validate(d)
        d=copy.deepcopy(self.data); d['envelope_mm']['z']=6000
        with self.assertRaises(ValueError): bp.validate(d)

    def test_manifest_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'obra-com-mezanino'/'model.json'; path.parent.mkdir(); path.write_bytes(EXAMPLE.read_bytes())
            bp.build(path); self.assertTrue(bp.build(path,check=True))
            manifest=json.loads((path.parent/'manifest.json').read_text())
            self.assertEqual(manifest['revisao'],'R24')
            for rel,meta in manifest['files'].items():
                b=(path.parent/rel).read_bytes()
                self.assertEqual(meta['sha256'],hashlib.sha256(b).hexdigest())
                self.assertEqual(meta['size'],len(b))

if __name__=='__main__': unittest.main()
