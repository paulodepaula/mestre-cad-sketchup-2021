#!/usr/bin/env python3
"""Gera DXF 2D de referencia (planta + lateral) do exemplo JSON.
Requer: pip install ezdxf. Nao faz dimensionamento estrutural.
"""
import json
import math
from pathlib import Path
import sys
import ezdxf


def base_doc():
    doc = ezdxf.new('R2010', setup=True)
    doc.header['$INSUNITS'] = 4   # mm
    doc.header['$MEASUREMENT'] = 1
    for name, color in [('MC_PISO', 7), ('MC_PILARES', 3), ('MC_COBERTURA', 4), ('MC_EIXOS', 8), ('MC_COTAS_GRAFICAS', 2)]:
        doc.layers.new(name=name, dxfattribs={'color': color})
    return doc


def rect(msp, xmin, ymin, xmax, ymax, layer):
    msp.add_lwpolyline([(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)],
                       close=True, dxfattribs={'layer': layer})


def line(msp, start, end, layer):
    msp.add_line(start, end, dxfattribs={'layer': layer})


def text(msp, content, at, height=90, layer='MC_COTAS_GRAFICAS'):
    msp.add_text(content, dxfattribs={'height': height, 'insert': at, 'layer': layer})


def render(data, folder):
    if data['unidades'] != 'mm' or data['schema'] != 'mestre-cad-geometria-v1':
        raise ValueError('Contrato JSON invalido')
    width = float(data['envelope_mm']['x'])
    depth = float(data['envelope_mm']['y'])
    elements = data['elementos']
    posts = [e for e in elements if e['tipo']=='caixa' and e['tag']=='PILARES_ESTUDO']
    roof = next(e for e in elements if e['id']=='COB')
    roof_pts = roof['pontos_mm']
    roof_front = float(roof_pts[0][2])
    roof_back = float(roof_pts[-1][2])
    rise = roof_back-roof_front

    plan_doc = base_doc()
    msp = plan_doc.modelspace()
    rect(msp, 0, 0, width, depth, 'MC_PISO')
    for p in posts:
        x,y,z = p['origem_mm']
        dx,dy,dz = p['dimensoes_mm']
        rect(msp,x,y,x+dx,y+dy,'MC_PILARES')
    for x in (0, width):
        line(msp, (x,-150), (x,-450), 'MC_COTAS_GRAFICAS')
    line(msp, (0,-300), (width,-300), 'MC_COTAS_GRAFICAS')
    text(msp, f'{width:.0f} mm', (width/2-260,-260))
    for y in (0,depth):
        line(msp, (-150,y),(-450,y),'MC_COTAS_GRAFICAS')
    line(msp,(-300,0),(-300,depth),'MC_COTAS_GRAFICAS')
    text(msp,f'{depth:.0f} mm',(-1000,depth/2))
    text(msp,'ESTUDO R00 - PLANTA / MEDIDAS EM mm',(0,depth+350),height=120)
    plan_out = folder/'oficina_4x6_planta_R00.dxf'
    plan_doc.saveas(plan_out)

    side_doc = base_doc()
    msp = side_doc.modelspace()
    line(msp, (0,0),(depth,0), 'MC_PISO')
    line(msp, (0,roof_front),(depth,roof_back), 'MC_COBERTURA')
    for p in posts:
        x,y,z = p['origem_mm']
        dx,dy,dz = p['dimensoes_mm']
        if x != 0: continue # mostra linha de pilares de um lado
        rect(msp,y,0,y+dy,dz,'MC_PILARES')
    text(msp, f'Caimento referencia: {rise:.0f} mm / {depth:.0f} mm = {rise/depth*100:.1f}%', (100,roof_back+300))
    text(msp,'ESTUDO R00 - ELEVACAO LATERAL / mm',(0,-350),height=120)
    side_out = folder/'oficina_4x6_lateral_R00.dxf'
    side_doc.saveas(side_out)
    return plan_out,side_out


if __name__ == '__main__':
    file = Path(sys.argv[1])
    output_folder = Path(sys.argv[2])
    output_folder.mkdir(parents=True, exist_ok=True)
    print('\n'.join(map(str, render(json.loads(file.read_text(encoding='utf-8')),output_folder))))
