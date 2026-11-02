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
- O proprietario confirmou a oficina no lado **B-C** e informou que mover o conjunto para a esquerda pode provocar interferencia com o portao. Por isso **nao adotar afastamento lateral arbitrario**; estudar alinhamento proximo ao limite B-C, sujeito a verificacao de divisa, recuos legais, drenagem e manutencao.
- A distancia lateral efetiva entre a cobertura/passarela e o limite B-C deve ser medida em campo, sobretudo junto ao muro existente; falta tambem confirmar o posicionamento longitudinal da construcao na faixa do portao.
- Portao deslizante na frente da rua para a direita, com ocupacao informada de 300 mm alem da face interna do muro, **nao define recuo suficiente**.
- Para futura implantacao unificada, converter origem local da R04 para deslocamentos `(x_implantacao_mm,y_implantacao_mm)` e verificar a orientacao real da cobertura/passarela e os limites. Nao copiar a origem (0,0) da R04 diretamente para o ponto A.

## Regras
- Nao foi alterado `model.json`, nem os arquivos CAD derivados da R04, para desenhar a base T01.
- Nao ha desenho de muros, casa existente, acesso de veiculos ou portao real dimensionados nesta planta.
- A linha da frente da rua **NAO determina automaticamente onde fica a entrada funcional da oficina**. Antes de desenhar fachada, definir se a entrada da oficina olha para a rua ou para o fundo do lote.
- Contorno geodesico estimativo e estudo de implantacao; verificar com levantamento topografico e regras de recuo aplicaveis.

## Condicionantes informados pelo proprietario - muro e portao

- **B-C e o lado direito olhando da rua para os fundos.** Ha um muro com aproximadamente **4.800 mm de altura** ao longo de todo o quintal nesse lado, conforme informado pelo proprietario. A altura e do muro existente, nao da oficina.
- O portao existente fica na frente A-B e **corre para a direita**, ocupando a lateral onde se pretende a obra. Sua saliencia para o interior da face do muro frontal foi informada como **300 mm**, ainda sem planta cotada da folha, trilhos, motor e percurso aberto.
- Segundo o proprietario, **afastar a oficina do lado B-C para o centro do lote interfere na area do portao**. Assim, nao mover a construcao lateralmente para impor um corredor adicional. A passarela nominal de 1m ja faz parte da faixa geral de 5m da R04 (oficina 4m + passarela 1m).
- A entrada funcional da oficina foi informada como **voltada para os fundos do terreno C-D**; isto se refere ao acesso, e nao autoriza inverter a geometria ativa R04 ou restabelecer a R05 desfeita.
- A distancia de **0,30 m** mencionada pelo proprietario como recuo precisa ser associada explicitamente a um par de superficies (muro frontal, portao, oficina) no levantamento. **Nao confundir** com a ocupacao de 0,30m do portao nem aprovar como recuo normativo.
- O muro vizinho **nao pode ser assumido como apoio estrutural** de vigas, terças ou cobertura. A cobertura existente do estudo cai para o lado B-C (5% ilustrativos), exigindo futura solucao de calha/drenagem que nao descarregue agua na propriedade vizinha.
- Deixar pendente a posicao global X/Y da oficina, a folga real da cobertura em relacao ao muro, a faixa de deslizamento do portao e as restricoes municipais de afastamento, sem alterar `model.json` nem `T01-planta-base.dxf` antes dessas conferencias.
