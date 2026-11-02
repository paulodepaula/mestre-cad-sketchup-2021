# I01 - Implantacao no terreno (base para futura R05)

**ESTUDO NAO EXECUTIVO. A geometria ativa continua R04, 42 elementos.** A antiga R05 com fachada foi desfeita e nao foi restaurada. Este trabalho nao modificou telhado nem qualquer elemento do modelo.

## Posicionamento
- Frente do terreno: **A-B**, aproximadamente 10,20m. Fundos do terreno: **C-D**, aproximadamente 10,47m.
- Muro alto existente a direita olhando da rua: **B-C**, comprimento aproximado 37,02m e altura informada 4,80m.
- Frente funcional da oficina: **voltada para C-D**, ou seja, para os fundos.
- Oficina de 4x6m (24m2): **a direita** na faixa junto ao muro B-C.
- Passarela coberta de 1x6m (6m2): **a esquerda**, voltada ao centro do terreno.
- Cobertura de 5x6m (30m2): borda direita alinhada ao lado B-C e avancando 1m a esquerda.
- A faixa nominal de 300mm, medida desde o muro frontal A-B, sera destinada ao portao existente quando aberto.

## Transformacao CAD
A R04 foi girada rigidamente em planta, sem espelhar ou alterar sua geometria. O giro e de aproximadamente 180 graus no sistema do terreno, com pequeno ajuste de 1.806 grau para acompanhar a inclinacao da linha B-C do KMZ.

Formula para os pontos R04 (x,y): `P_lote = F + u*x + v*(6000-y)`. Vetor unitario u para dentro do lote = (-0.999502995, 0.031524013); v ao longo de B-C = (0.031524013, 0.999502995); F = (10205.5, 300) mm. O coordenada Z e mantida.

A borda direita dianteira da cobertura no terreno e 10205.5, 300mm (Y=300mm). A borda esquerda dianteira e 5207.9, 457.6mm. Como o muro B-C e ligeiramente inclinado, o recuo frontal no lado esquerdo e ~457.6mm, e nao 300mm uniformemente.

## Arquivos
- [R05-implantacao-estudo.dxf](R05-implantacao-estudo.dxf): contorno do lote, oficina, passarela, telhado, mezanino, escada e colunas numeradas em layers editaveis.
- [R05-implantacao-estudo.json](R05-implantacao-estudo.json): orientacao, transformacao rigida e pontos cotados.
- A planta nao substitui o `model.json` ativo R04.

## Alertas
- **Afastamento zero a B-C e apenas hipotese geometrica**, nao permissao de construir junto a divisa. Conferir normas municipais, impermeabilizacao, calha, agua pluvial e manutencao. O muro vizinho nao e suporte para o telhado.
- Os 300mm devem ser aferidos desde a face interna real do muro e verificados com todo o portao aberto (trilho, motor, batentes e folgas).
- Levantar a garagem, casa e edificacoes existentes para checar o acesso de veiculos. O KMZ nao representa limites legais/topografia certificada.
- Nao ha dimensionamento estrutural nem modificacao no telhado, colunas, vigas ou mezanino R04.
