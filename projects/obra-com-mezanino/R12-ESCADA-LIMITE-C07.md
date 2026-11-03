# R12 - Reserva da escada sem ultrapassar a face da C07

**Escopo: posicionamento em planta, nao dimensionamento de escada.** A R11 possui somente a face `ESCADA_RES`, sem degraus, longarinas, corrimaos ou patamares intermediarios. A R12 nao inventa uma escada executiva nem comprime degraus existentes.

## Referencia adotada
A coluna do mezanino ao lado da escada e **C07**. Seu alinhamento externo, voltado para os fundos C-D do lote, e **Y=5621mm** (origem Y5521 + secao 100). C10 e o plano dos vidros superiores coincidem com essa face. A referencia escolhida e a FACE, nao o eixo central Y5571.

## Alteracao
- Antes: reserva X9461..10361, Y2421..6621, Z0, dimensoes 900x4200mm.
- Depois: reserva **X9461..10361, Y2421..5621, Z0**, dimensoes **900x3200mm**.
- A extremidade voltada para C-D recua **1000mm**, eliminando o avanco alem da linha da coluna.
- A borda de chegada ao patamar continua em **Y2421mm**. O patamar existente permanece de Y621 a Y2421, com topo em **Z2715mm**.
- Reduz-se o espaco disponivel para estudar a escada; nao se afirma que um lance reto executavel caiba em 3200mm.

## Preservacao
Todos os outros 100 elementos da R11 sao preservados integralmente, incluindo C01-C08/C10, V01-V13, grade interna 50x50, piso/patamar, vidros/soleiras, telhado, terreno e muro B-C. Sem novas alteracoes de secoes, niveis, materiais, extensao ou workflow. Modelo continua com **101 elementos**.

## Pendencia detectada na conferência
A C02 existente ocupa X10311..10461 e Y3571..3721. Ela invade em planta **50mm** da faixa nominal da escada, que termina em X10361; restam **850mm** nesse trecho, antes de descontar corrimaos/longarinas. Essa interferencia ja existia na R11 e nao foi corrigida deslocando pilares sem pedido. Continua registrada explicitamente em `parametros_estudo_mm.escada_r12`.

Para transformar esta reserva em escada funcional, sera preciso estudar degraus, largura util, inclinação, altura livre, acesso inferior, eventual mudanca de direcao, guarda-corpos e a interferencia C02. A posicao por si so nao aprova conformidade, seguranca ou fabricacao.

## Verificacao
Testes comparam a R12 com o snapshot exato R11: somente `ESCADA_RES` muda entre os elementos; a reserva termina na face C07/C10, chega ao patamar sem alterar a sua geometria, e preserva o nivel de referencia 2715mm. Continuam os testes de contato/nao-interpenetracao da grade, unidades, coplanaridade, DXF/DAE e manifesto.

Fonte anterior arquivada pelo blob original em `historico/model-R11.json`. Atualizacao exclusivamente via GitHub para sincronizacao pelo plugin.
