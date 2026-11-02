# R05 - Terreno T01 e muro B-C integrados ao SketchUp

**O modelo JSON principal foi atualizado e sincronizavel diretamente pelo plugin SketchUp Mestre CAD 2021.**

## Componentes visiveis no SketchUp apos sincronizar
- `T01_TERRENO`: face do terreno completo (~382,15m2 KMZ, aproximado), pontos no referencial girado:
  A (270,0), B (10461,321), C (10461,37341), D (0,36990) mm.
- `MURO_BC`: grupo-face vertical no trecho B-C com **4800 mm de altura**, sem espessura porque nao foi informada.
- `PISO_T`: oficina 4000x6000mm na direita do lote junto a B-C.
- `PASSE`: passarela 1000x6000mm do lado esquerdo, voltada ao centro do lote.
- `COB_R03` e `V01..V09`: mesmas geometrias relativas, somente reposicionadas no terreno.
- `C01..C09`, `V01..V12`: todas as identificacoes mantidas. Sao marcadores de estudo, nao pecas calculadas.

## Transformacao geometrica do projeto original
Para fazer as caixas continuarem validas como `caixa` no plugin instalado (sem atualizar extensao), o sistema global foi alinhado matematicamente com a reta B-C. Isto coloca o muro na reta vertical X=10461mm.

Todos os elementos originais R04 foram girados em **180 graus** na planta e transladados sem redimensionamento:
- x_global = 10461 - x_original_R04
- y_global = 6621 - y_original_R04
- z_global = z_original_R04

Para prismas de `largura=w, profundidade=d`, a origem global e: `(10461-x-w, 6621-y-d, z)`. As dimensoes dos prismas nao mudam.
O limite do terreno gera envelope **X 10461 × Y 37341 × Z 5600 mm**.

## Posicionamento de estudo
- Vista da rua: **direita B-C** (muro existente), esquerda D-A.
- O telhado ocupa X 5461..10461; a **sobra de 1 m** esta no lado esquerdo da oficina (X 5461..6461).
- Recuo junto ao muro da rua: **300 mm no canto direito** da cobertura, intervalo Y 321..621; menor recuo nos demais pontos NAO foi levantado em campo.
- Frente funcional da oficina fica voltada para **C-D**.
- Muro do vizinho e planta do KMZ apenas orientam estudo, nao validam legalmente afastamento zero ou uso estrutural do muro.
- Portao, motor, trilho, calha e recuos oficiais ainda precisam de verificacao.

## Fluxo obrigatorio
Consultar [AGENTS.md](AGENTS.md): **desenvolvimento no GitHub e somente sincronizacao via plugin no SketchUp. Sem desenho manual.**

Historico R04 em [historico/model-R04.json](historico/model-R04.json). A R05 anterior desfeita permanece em `historico/model-R05-desfeito.json` e NAO foi restaurada.
