# Levantamento T01 - Terreno conforme novo KMZ

**Fonte dimensional atual:** arquivo KMZ corrigido informado pelo proprietario: `Caminho sem titulo(2).kmz`.

## Resultado do calculo geodesico WGS84

| Trecho | Comprimento |
|---|---:|
| A-B | 10,20 m |
| B-C | 37,02 m |
| C-D | 10,47 m |
| D-A | 36,99 m |
| Area do poligono | **382,15 m2** |
| Perimetro | **94,67 m** |

O KMZ e um `LineString` com 5 posicoes, sendo a quinta igual a primeira; 4 vertices unicos definem o poligono fechado. O calculo da area considera fecho A-B-C-D-A. A medicao anterior, 271,31 m2 e aproximadamente 26 m de profundidade, **foi substituida** pelo novo contorno.

## Referencia CAD local
Para permitir importar no futuro um desenho de implantacao com coordenadas locais, o arquivo [T01-contorno.json](terreno/T01-contorno.json) contem quatro vertices no sistema relativo:

- Origem A = (0,0) mm.
- Eixo X no sentido A->B, eixo Y no sentido do interior do quadrilatero, sem identificar o norte nem a frente.
- Aproximacoes: A (0,0), B (10196,0), C (11363,37001), D (896,36980), em mm.
- Valores derivados de geodesia e convertidos a coordenadas locais; nao devem ser confundidos com limites legais.

**Privacidade:** coordenadas GPS exatas e KMZ original **nao foram publicados** no repositorio GitHub publico. Ha somente medidas e um contorno em referencia local.

## Compatibilizacao com a obra
A oficina continua 4000 x 6000 mm, passarela de 1000 mm e revisao geométrica R03. Nao mover a edificacao nem criar deslocamentos na maquete sem identificar qual segmento (AB ou CD) esta de frente para a rua e definir recuos/margens/circulacao.

A localizacao legal e as divisas reais exigem confrontacao com documentacao oficial e medicao topografica em campo. O KMZ, mesmo marcado como correto pelo proprietario, e referencia de estudo, nao topografia homologada.
