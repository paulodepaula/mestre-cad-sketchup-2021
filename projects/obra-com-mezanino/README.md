# Obra com mezanino - R03 (estudo, NAO EXECUTIVO)

O `model.json` e a fonte de geometria em mm. GitHub Actions gera `cadcraft/planta.dxf`, `cadcraft/elevacoes.dxf`, `sketchup/modelo.dae` e `manifest.json`.

## Dimensoes e hipoteses
- Oficina 4000 x 6000 mm e passarela direita de 1000 mm de largura: definidas pelo proprietario.
- Portao existente avanca 300 mm para dentro do muro frontal (medida informada). Nao equivale a recuo aprovado.
- Mezanino proposto 3000 x 4000 mm, topo Z2850, piso representativo 160 mm; escada somente reserva 900 x 4200.
- Altura de estudo Z5600, inclinacao ilustrativa 5%, marcadores de secoes e vigas: nao dimensionados.

## Cobertura em balanco
- Retirados os tres pilares e viga longitudinal externos da passarela do modelo R02.
- R03 modela tres travessas transversais inclinadas de estudo ate X5000, a partir de uma linha de apoio de referencia no limite X4000 da oficina. Balanco nominal 1000 mm, **sem coluna na extremidade**.
- Com a extensao 1.4.1 as travessas inclinadas sao representadas por 6 faces por elemento formando casca, nao perfis estruturais.
- Nao utilizar para fabricar: capacidade de vigas, rigidez de ligacoes, vento, deflexao e fundacoes pendentes de projeto e ART/RRT.

## Historico e integracao
R00/R01/R02 preservados em `historico/`. Detalhes em [R03-BALANCO-COBERTURA.md](R03-BALANCO-COBERTURA.md).
Extensoes > Mestre CAD 2021 > Sincronizar arquivos CAD do GitHub > Importar projeto sincronizado > Conferir grupo selecionado. O arquivo SKP fica apenas local no SketchUp.

## Terreno - levantamento T01 (KMZ revisado)

- **Area geodesica de referencia: 382,15 m2.** Lados: AB 10,20 m, BC 37,02 m, CD 10,47 m, DA 36,99 m.
- Este levantamento **substitui o de 271,31 m2**; os limites sao estimados a partir de Google Earth, sem certidao topografica.
- Dados e contorno local sem coordenadas GPS em [TERRENO-T01.md](TERRENO-T01.md) e [`terreno/T01-contorno.json`](terreno/T01-contorno.json).
- Frente A-B (10,20 m) confirmada; olhando da rua, B-C e a lateral direita prevista para a oficina. Geometria R03 ainda nao movida: faltam cotas dos recuos, circulacao e folga do portao.
