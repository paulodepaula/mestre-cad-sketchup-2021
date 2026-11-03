# R14 - Escada em U modelada em 3D

**ESTUDO GEOMETRICO, NAO EXECUTIVO.** Na R13 havia somente ESCADA_RES, uma face no piso. A R14 acrescenta a geometria efetiva dos degraus e patamar para visualizacao sincronizada. Nao houve alteracao da extensao ou dos materiais.

## Por que o espaco reservado mudou
A reserva anterior era 900 x 3200 mm para um desnivel de 2715 mm. Um lance reto com 16 espelhos de 169,6875 mm e 15 pisos de 300 mm precisaria de 4500 mm de desenvolvimento, antes do patamar. Nao foi comprimida a profundidade dos degraus para forcar o encaixe.

Seguindo a diretriz anterior do proprietario de admitir dois sentidos quando necessario, foi adotado um estudo em U: dois lances paralelos e patamar de retorno. A largura total aumenta para dentro da oficina, e a escada nao ultrapassa a linha frontal C07/C10.

## Cotas da escada
| Item | Geometria adotada no estudo |
|---|---|
| Desnivel total | 2715 mm |
| Espelhos | 16 iguais, 169,6875 mm cada |
| Pisos de degraus | 14, de 900 x 300 mm, 7 em cada lance |
| Espelhos 8 e 16 | chegada ao patamar intermediario e ao mezanino |
| Patamar intermediario | 2100 x 1000 mm, topo Z1357,5 |
| Largura entre faces das longarinas | 900 mm em cada lance |
| Distancia entre faces internas dos lances | 200 mm |
| Envelope de estudo | X8261..10361; Y2421..5521 |
| Linha limite da coluna | face C07/C10 em Y5621 |
| Chegada superior | Y2421, Z2715, encontra patamar existente |
| Lance inferior | sobe no sentido +Y; X8311..9211 |
| Lance superior | sobe no sentido -Y; X9411..10311 |
| Entrada no terreo | lado Y2421 do lance inferior, acessivel pelo lado livre da oficina |

O topo dos degraus e os espelhos foram calculados com 2715/16 sem arredondamentos acumulados. O envelope de 30mm do degrau nao especifica chapa macica de aco: material, bandeja, enrijecedores, acabamento antiderrapante e fixacoes permanecem pendentes.

## Impacto no piso e na estrutura do mezanino
Esta revisao NAO preserva integralmente o piso: a abertura adicional retira **3,7275 m2** de paineis, incluindo o ajuste da faixa junto a C07. A area geometrica passa de **16,725 para 12,9975 m2**, antes de descontar outros recortes e circulacao.

- MEZ_PRINCIPAL passa a representar a faixa X6461..8261, mantendo Z2690..2715.
- MEZ_FRENTE_R14 completa X8261..9461, Y621..2421.
- MEZ_FAIXA_R14 e um arremate estreito, NAO circulavel, sobre V05, sem atravessar C07.
- MEZ_PATAMAR permanece intacto.
- **V03** permanece em X9361..9461 e Y621..2421; o restante do trecho anterior foi retirado do ESTUDO para liberar o vazio.
- **V14** contorna o vazio em X8161..8261, Y2421..5521.
- **V15** e o novo cabecalho entre V04 e V03, X6561..9361, Y2321..2421.
- Oito trechos G11_ML02 foram removidos; oito travessas principais foram encurtadas, duas barras foram ajustadas e uma continuacao G14 foi criada. A grade restante tem 40 barras, com secao externa de estudo 50x50 e parede ainda indefinida.

**Essas mudancas alteram a distribuicao de cargas. V03, V14, V15 e todas as ligacoes precisam de novo calculo. Este arquivo NAO autoriza o corte ou a modificacao de uma estrutura executada.**

## Apoios, longarinas e guardas
O patamar intermediario tem quadro de apoio e quatro suportes ate o terreo, todos com perfis apenas representativos e fundacoes nao definidas. As quatro longarinas sao faces laterais, sem espessura fabricavel; nao fingem um perfil comercial dimensionado. Os planos de guarda indicam bordas a proteger e altura de referencia 1100mm, mas corrimaos preensiveis, montantes, rodapes, encontros, pequenas transicoes e resistencias ainda devem ser detalhados. Nao considerar a escada pronta para uso.

## Elementos preservados
Pilares C01-C08/C10 (inclusive C02 100x100x3), V01/V02 da cobertura, V04/V05/V06/V10/V11/V12, V07/V08/V09/V13, telhado COB_R03, terreno T01, muro B-C, vidros e soleiras. O vidro continua sem fume. Nao se alterou o recuo frontal nem a oficina de 4000x6000 mm.

## Referencia tecnica consultada
CBMRO, IT11/2023, itens 5.7.2, 5.7.3 e 5.7.5, disponivel na pagina de instrucoes vigentes. A relacao geometrica calculada e 2h+b = 639,375 mm, dentro da faixa 630..640mm indicada na referencia. O documento estabelece condicoes especificas para escadas de uso restrito; o enquadramento real do escritorio, lotacao, acessibilidade e demais exigencias ainda deve ser confirmado por profissional habilitado. Nao ha declaracao de conformidade integral.

Fonte: https://www.cbm.ro.gov.br/wp-content/uploads/2024/01/IT-11_-_SADAS_DE_EMERGNCIA.pdf
Pagina institucional: https://www.cbm.ro.gov.br/?page_id=694

## Verificacoes automatizadas
- Registros das alteracoes e comparacao com a R13 original arquivada.
- 150 elementos, limite atual do importador; 89 caixas e 61 faces.
- 16 espelhos uniformes e 14 pisos; patamares em Z1357,5 e Z2715.
- Encaixe no envelope, sem avancar da linha C07, e chegada no patamar.
- Contatos da grade e das novas vigas de contorno.
- Ausencia de penetracao das caixas novas nas demais caixas modeladas.
- Amostragem de altura livre em pontos dos degraus e patamar. A amostragem NAO substitui verificacao completa de percurso, corrimaos, acabamentos e tolerancias.
- XML COLLADA, unidades, DXF, manifesto, hashes e testes negativos de geometria/arquivos adulterados.

Arquivo anterior integral: historico/model-R13.json. Mantido o fluxo exclusivo GitHub -> sincronizacao pelo plugin.
