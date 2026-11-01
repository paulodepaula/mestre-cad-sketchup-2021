# Obra com mezanino - estudo geometrico R00

**Status: estudo ilustrativo 4.000 x 6.000 mm, NAO e projeto executivo nem mezanino dimensionado.**

## Fonte do projeto

`model.json` e a fonte das medidas e posicoes. Edite o JSON e publique na branch `main`. O workflow `Gerar arquivos CAD a partir do projeto` valida o modelo, gera e versiona:

- `cadcraft/planta.dxf`: geometria 2D da planta em milimetros, DXF ASCII R12.
- `cadcraft/elevacoes.dxf`: elevacoes frontal/lateral em milimetros, DXF ASCII R12.
- `sketchup/modelo.dae`: geometria 3D COLLADA, unidade declarada em milimetros, eixo Z vertical.
- `manifest.json`: arquivo verificavel com SHA-256 e tamanho de cada arquivo.

Os desenhos podem ser abertos no CadCraft e o DAE pode ser importado no SketchUp 2021. A extensao Mestre CAD 2021 v1.3.0 tambem sincroniza estes arquivos diretamente do GitHub e importa o JSON como grupos SketchUp. Depois e possivel salvar localmente o modelo editavel `.skp` no proprio SketchUp.

**Nao existe um `.skp` nativo gerado no GitHub neste MVP:** requer o SDK C oficial autorizado e um runner Windows/macOS configurado. Nao renomear DAE para SKP. Nao existe conversao DWG sem programa conversor licenciado/verificado.

Os pilares ilustrativos de 100 x 100 mm nao foram dimensionados e a cobertura nao teve verificada sua estabilidade ou fixacao. Exigem validacao por profissional habilitado e ART/RRT conforme aplicavel.
