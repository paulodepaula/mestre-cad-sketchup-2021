# Obra com mezanino - R02 (estudo dimensional, NAO EXECUTIVO)

**Fonte de verdade:** `model.json` em milimetros. O pipeline gera `cadcraft/planta.dxf`, `cadcraft/elevacoes.dxf`, `sketchup/modelo.dae` e `manifest.json`.

## Medidas definidas vs hipoteses
- Dimensoes principais informadas: 4000 x 6000 mm (24 m2), passarela a direita de 1000 mm de largura.
- Mezanino 3000 x 4000 mm em Z=2850: hipotese. Escada 900 x 4200: reserva sem calculo.
- Altura de referencia do modelo 5600 mm, marcadores de pilares e vigas de 100 mm, cobertura a 5% e laje de 160 mm: **hipoteses apenas de representacao volumetrica**.
- Portao com interferencia de 300 mm apos muro: medida informada; nao equivale a recuo aprovado.
- Planta, posicoes, alturas, pilares e cobertura **nao foram liberados para construcao**. Engenharia, arquitetura e ART/RRT devem validar.

## Historico e pendencias
- R00 em `historico/model-R00.json`, R01 em `historico/model-R01.json`.
- Especificacao, coordenadas e alertas em [R02-VOLUMETRIA-ESTUDO.md](R02-VOLUMETRIA-ESTUDO.md).
- Aspectos do terreno e as medidas de implantacao seguem pendentes.

## SketchUp 2021 / CadCraft
Extensoes > Mestre CAD 2021 > Sincronizar arquivos CAD do GitHub; Importar projeto sincronizado; Conferir grupo selecionado; Salvar copia SKP do projeto sincronizado. O SKP so fica no computador. Abrir DXF no CadCraft. A auditoria mede posicoes e envelopes e nao valida estrutura.
