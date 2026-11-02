#!/usr/bin/env python3
"""Build deterministic DXF and COLLADA files from Mestre CAD geometry v1 JSON.

No proprietary CAD tool or GUI is needed. Never labels a file as .skp or .dwg.
Usage: python tools/build_project.py projects/obra-com-mezanino/model.json [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

SCHEMA = 'mestre-cad-geometria-v1'
SYNC_SCHEMA = 'mestre-cad-sync-v1'
OUTPUTS = ('cadcraft/planta.dxf', 'cadcraft/elevacoes.dxf', 'sketchup/modelo.dae')
NS = 'http://www.collada.org/2005/11/COLLADASchema'
ET.register_namespace('', NS)


def fail(message):
    raise ValueError(message)


def number(value, label, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        fail(f'{label}: deve ser numero finito')
    if value <= 0 if positive else value < 0:
        fail(f'{label}: medida invalida')
    if value > 500000:
        fail(f'{label}: excede 500000 mm')
    return float(value)


def vec3(value, label, *, positive=False):
    if not isinstance(value, list) or len(value) != 3:
        fail(f'{label}: vetor 3D invalido')
    return tuple(number(x, label, positive=positive) for x in value)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def validate(data):
    if not isinstance(data, dict) or data.get('schema') != SCHEMA or data.get('unidades') != 'mm':
        fail('Schema/unidades nao suportados (use mestre-cad-geometria-v1 em mm)')
    if not isinstance(data.get('nome'), str) or not data['nome'].strip():
        fail('Nome do projeto ausente')
    if not isinstance(data.get('revisao'), str) or not re.fullmatch(r'R\d{2,4}', data['revisao']):
        fail('Revisao deve ser R00, R01, ...')
    bounds = data.get('envelope_mm')
    if not isinstance(bounds, dict):
        fail('envelope_mm ausente')
    envelope = tuple(number(bounds.get(k), 'envelope.'+k, positive=True) for k in ('x', 'y', 'z'))
    elements = data.get('elementos')
    if not isinstance(elements, list) or not 1 <= len(elements) <= 150:
        fail('Elementos devem conter entre 1 e 150 itens')
    seen, minima, maxima = set(), [float('inf')]*3, [-float('inf')]*3
    for i, item in enumerate(elements):
        if not isinstance(item, dict):
            fail(f'Elemento {i} invalido')
        key = item.get('id')
        if not isinstance(key, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,47}', key) or key in seen:
            fail(f'ID ausente/duplicado/invalido: {key}')
        seen.add(key)
        if not isinstance(item.get('nome'), str) or not item['nome'].strip():
            fail(f'{key}: nome invalido')
        if not isinstance(item.get('tag'), str) or not re.fullmatch(r'[A-Z][A-Z0-9_]*', item['tag']):
            fail(f'{key}: tag invalida')
        if item.get('tipo') == 'caixa':
            origin = vec3(item.get('origem_mm'), key+'.origem')
            dims = vec3(item.get('dimensoes_mm'), key+'.dimensoes', positive=True)
            pts = [origin, tuple(origin[j]+dims[j] for j in range(3))]
        elif item.get('tipo') == 'face':
            raw = item.get('pontos_mm')
            if not isinstance(raw, list) or len(raw) != 4:
                fail(f'{key}: face deve possuir 4 vertices')
            pts = [vec3(v, key+'.ponto') for v in raw]
            a,b,c,d=pts
            u = tuple(b[j]-a[j] for j in range(3))
            v = tuple(c[j]-a[j] for j in range(3))
            n = cross(u,v)
            length=math.sqrt(sum(t*t for t in n))
            if length < 0.5:
                fail(f'{key}: face degenerada')
            offset=tuple(d[j]-a[j] for j in range(3))
            if abs(sum(n[j]*offset[j] for j in range(3)) / length) > 0.5:
                fail(f'{key}: face nao coplanar')
        else:
            fail(f'{key}: tipo desconhecido')
        lo = [min(p[j] for p in pts) for j in range(3)]
        hi = [max(p[j] for p in pts) for j in range(3)]
        for j in range(3):
            if lo[j] < -0.5 or hi[j] > envelope[j] + 0.5:
                fail(f'{key}: fora do envelope')
            minima[j], maxima[j] = min(minima[j], lo[j]), max(maxima[j], hi[j])
    if any(abs(minima[j]) > 0.5 or abs(maxima[j] - envelope[j]) > 0.5 for j in range(3)):
        fail('Envelope incoerente com o conjunto de elementos')
    return envelope


def fmt(x):
    if not math.isfinite(x):
        fail('Coordenada nao finita')
    out = f'{x:.6f}'.rstrip('0').rstrip('.')
    return '0' if out in ('', '-0') else out


def box_vertices(item):
    x,y,z = map(float, item['origem_mm'])
    w,d,h = map(float, item['dimensoes_mm'])
    return [(x,y,z),(x+w,y,z),(x+w,y+d,z),(x,y+d,z),
            (x,y,z+h),(x+w,y,z+h),(x+w,y+d,z+h),(x,y+d,z+h)]


def projected_outline(item, axes):
    if item['tipo'] == 'face':
        points = [tuple(map(float,p)) for p in item['pontos_mm']]
    else:
        points = box_vertices(item)
    xy = [(p[axes[0]],p[axes[1]]) for p in points]
    if item['tipo']=='face':
        return xy
    lo = (min(p[0] for p in xy), min(p[1] for p in xy))
    hi = (max(p[0] for p in xy), max(p[1] for p in xy))
    if abs(hi[0]-lo[0]) < 1e-7 or abs(hi[1]-lo[1]) < 1e-7:
        return []
    return [(lo[0],lo[1]),(hi[0],lo[1]),(hi[0],hi[1]),(lo[0],hi[1])]


def dxf(data, mode):
    lines=[]
    def pair(code, value):
        lines.extend((str(code), str(value)))
    def line(a,b,layer):
        pair(0,'LINE');pair(8,layer)
        pair(10,fmt(a[0]));pair(20,fmt(a[1]));pair(30,'0')
        pair(11,fmt(b[0]));pair(21,fmt(b[1]));pair(31,'0')
    def text(value,x,y,h=120):
        pair(0,'TEXT');pair(8,'MC_ANOTACOES');pair(10,fmt(x));pair(20,fmt(y));pair(30,'0')
        pair(40,fmt(h));pair(1,value)
    pair(0,'SECTION');pair(2,'HEADER');pair(9,'$ACADVER');pair(1,'AC1009')
    pair(9,'$MEASUREMENT');pair(70,1);pair(0,'ENDSEC')
    pair(0,'SECTION');pair(2,'ENTITIES')
    en=data['envelope_mm']; x,y,z=en['x'],en['y'],en['z']
    if mode=='planta':
        for el in data['elementos']:
            coords=projected_outline(el,(0,1))
            for i in range(len(coords)):
                if coords[i]!=coords[(i+1)%len(coords)]:
                    line(coords[i],coords[(i+1)%len(coords)],el['tag'])
        # Referencias visiveis no CAD 2D: colunas e vigas numeradas.
        # Vigas inclinadas V07-V09 possuem seis faces cada; rotular apenas _TOP.
        for el in data['elementos']:
            key = el['id']
            if re.fullmatch(r'C[0-9]{2}', key):
                coords = projected_outline(el, (0, 1))
                if coords:
                    text(key, coords[0][0]+130, coords[0][1]+130, 95)
            elif re.fullmatch(r'V[0-9]{2}', key) or re.fullmatch(r'V[0-9]{2}_TOP', key):
                coords = projected_outline(el, (0, 1))
                if coords:
                    label = key[:3]
                    midx = (min(p[0] for p in coords)+max(p[0] for p in coords))/2
                    midy = (min(p[1] for p in coords)+max(p[1] for p in coords))/2
                    text(label, midx, midy, 90)
        text('PLANTA ESTUDO '+data['revisao']+' - MM - NAO EXECUTIVO',0,-350)
        text('LARGURA '+fmt(x)+' mm',0,-550,90)
        text('PROFUNDIDADE '+fmt(y)+' mm',0,-720,90)
    elif mode=='elevacoes':
        offset=x+1500
        for el in data['elementos']:
            for ax, shift in [((0,2),0),((1,2),offset)]:
                coords=projected_outline(el,ax)
                for i in range(len(coords)):
                    a,b=coords[i], coords[(i+1)%len(coords)]
                    if a!=b:line((a[0]+shift,a[1]),(b[0]+shift,b[1]),el['tag'])
        text('FACHADA FRONTAL (X/Z) ESTUDO',0,-350)
        text('ELEVACAO LATERAL (Y/Z) ESTUDO',offset,-350)
    else:
        fail('Vista desconhecida')
    pair(0,'ENDSEC');pair(0,'EOF')
    return ('\n'.join(lines)+'\n').encode('ascii')


def dae(data):
    def q(tag):return '{'+NS+'}'+tag
    def sub(parent,tag,**kwargs):return ET.SubElement(parent,q(tag),{k:str(v) for k,v in kwargs.items()})
    root=ET.Element(q('COLLADA'),{'version':'1.4.1'})
    asset=sub(root,'asset');sub(asset,'created').text='2026-11-01T00:00:00';sub(asset,'modified').text='2026-11-01T00:00:00'
    sub(asset,'unit',name='millimeter',meter='0.001');sub(asset,'up_axis').text='Z_UP'
    lg=sub(root,'library_geometries');lvs=sub(root,'library_visual_scenes');vs=sub(lvs,'visual_scene',id='Scene',name='Scene')
    for idx,item in enumerate(data['elementos']):
        item_id=f'geo_{idx}_{item["id"]}'
        if item['tipo']=='caixa':
            verts=box_vertices(item)
            tris=[(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),
                  (1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]
        else:
            verts=[tuple(map(float,p)) for p in item['pontos_mm']]
            tris=[(0,1,2),(0,2,3)]
        g=sub(lg,'geometry',id=item_id,name=item['nome']);mesh=sub(g,'mesh')
        src=sub(mesh,'source',id=item_id+'-positions')
        farr=sub(src,'float_array',id=item_id+'-positions-array',count=str(len(verts)*3))
        farr.text=' '.join(fmt(x) for p in verts for x in p)
        common=sub(src,'technique_common');acc=sub(common,'accessor',source='#'+item_id+'-positions-array',count=str(len(verts)),stride='3')
        for axis in ('X','Y','Z'):sub(acc,'param',name=axis,type='float')
        vert=sub(mesh,'vertices',id=item_id+'-vertices');sub(vert,'input',semantic='POSITION',source='#'+item_id+'-positions')
        tri=sub(mesh,'triangles',count=str(len(tris)));sub(tri,'input',semantic='VERTEX',source='#'+item_id+'-vertices',offset='0')
        sub(tri,'p').text=' '.join(str(j) for face in tris for j in face)
        node=sub(vs,'node',id='node_'+str(idx),name=item['nome'],type='NODE')
        sub(node,'instance_geometry',url='#'+item_id)
    sc=sub(root,'scene');sub(sc,'instance_visual_scene',url='#Scene')
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)


def build(model_path:Path,check=False):
    data=json.loads(model_path.read_text(encoding='utf-8'))
    envelope=validate(data)
    base=model_path.parent
    outputs={'cadcraft/planta.dxf':dxf(data,'planta'),
             'cadcraft/elevacoes.dxf':dxf(data,'elevacoes'),
             'sketchup/modelo.dae':dae(data)}
    source=model_path.read_bytes()
    digest=lambda b: hashlib.sha256(b).hexdigest()
    meta={ 'schema':SYNC_SCHEMA, 'projeto':base.name, 'revisao':data['revisao'],
           'envelope_mm':{'x':envelope[0],'y':envelope[1],'z':envelope[2]},
           'source_sha256':digest(source),
           'files':{k:{'sha256':digest(v),'size':len(v)} for k,v in sorted({**outputs,'model.json':source}.items())}}
    outputs['manifest.json']=(json.dumps(meta,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
    for relative, content in outputs.items():
        dest=base/relative
        if check:
            if not dest.is_file() or dest.read_bytes()!=content:
                fail(f'Arquivo ausente ou desatualizado: {relative}')
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(content)
    print(f'PASS: {base.name} {data["revisao"]} / {len(data["elementos"])} elementos / X Y Z {envelope} mm / {"verificado" if check else "gerado"}')
    return outputs


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('model',type=Path)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    try:build(args.model,args.check)
    except (ValueError,KeyError,TypeError,FileNotFoundError,json.JSONDecodeError) as exc:
        print('FAIL:',exc,file=sys.stderr);sys.exit(1)
