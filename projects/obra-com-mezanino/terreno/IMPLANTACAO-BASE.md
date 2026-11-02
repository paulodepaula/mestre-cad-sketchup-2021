# Planta-base de implantacao do terreno T01

**Geometria do terreno reproduzida no DXF separado** [T01-planta-base.dxf](T01-planta-base.dxf). Unidades **milimetros (mm)**. A geometria estrutural do projeto ativo permanece **R04**, apos a reversao solicitada da R05.

## Lados e orientacao confirmados
- **A-B: FRENTE DA RUA** ~10,20 m, Y=0 em referencia local.
- **B-C: LATERAL DIREITA** ~37,02 m, olhando da rua para o fundo.
- **C-D: FUNDOS DO TERRENO** ~10,47 m, perto de Y=37.000 mm.
- **D-A: LATERAL ESQUERDA** ~36,99 m.
- Area geodesica de referencia **382,15 m2**.
- A na esquerda, B na direita da rua, C canto posterior direito, D posterior esquerdo. A referencia geodesica e estimativa do KMZ, nao levantamento topografico.

## Geometrias no desenho
- O contorno quadrilateral e o limite de estudo do terreno e ocupa as coordenadas locais A(0,0), B(10196,0), C(11363,37001), D(896,36980).
- Um **bloco isolado fora do terreno** e mostrado para referenciar o volume nominal de projeto: 4000x6000 mm de oficina e 1000x6000 mm da passarela. **NAO ESTA POSICIONADO NA OBRA.**
- A oficina permanece no **lado direito do terreno** como diretriz de projeto; faltam duas cotas de locacao: (1) distancia frontal entre muro da rua e eixo/face da obra; (2) afastamento lateral do limite B-C ate a borda direita da passarela.
- Portao deslizante na frente da rua para a direita, com ocupacao informada de 300 mm alem da face interna do muro, **nao define recuo suficiente**.
- Para futura implantacao unificada, converter origem local da R04 para deslocamentos `(x_implantacao_mm,y_implantacao_mm)` e verificar a orientacao real da cobertura/passarela e os limites. Nao copiar a origem (0,0) da R04 diretamente para o ponto A.

## Regras
- Nao foi alterado `model.json`, nem os arquivos CAD derivados da R04, para desenhar a base T01.
- Nao ha desenho de muros, casa existente, acesso de veiculos ou portao real dimensionados nesta planta.
- A linha da frente da rua **NAO determina automaticamente onde fica a entrada funcional da oficina**. Antes de desenhar fachada, definir se a entrada da oficina olha para a rua ou para o fundo do lote.
- Contorno geodesico estimativo e estudo de implantacao; verificar com levantamento topografico e regras de recuo aplicaveis.
