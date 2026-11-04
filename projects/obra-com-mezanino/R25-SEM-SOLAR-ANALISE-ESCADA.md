# R25 - remoção do solar e análise da inversão da escada

## Solar
Todos os elementos solares gerados pelo projeto foram removidos:
- superfícies fotovoltaicas;
- molduras;
- trilhos PV23.

A cobertura COB_R03 permanece sem alteração. O usuário utilizará seu próprio modelo de painéis.

## Escada
O pedido foi inverter o trecho curto do L para a parede oposta.

A geometria atual mostra:
- borda direita do lance principal: X=10361mm;
- parede lateral: X=10461mm;
- espaço disponível: **100mm**;
- trecho curto pretendido: aproximadamente **1000mm**.

Portanto, não é fisicamente possível simplesmente espelhar o trecho curto mantendo o lance principal no lugar. Para isso seria necessário deslocar o lance principal cerca de 900–1000mm para a esquerda, o que invade a projeção do mezanino atual.

A escada R24 foi preservada nesta revisão para evitar uma solução geométrica incoerente. A próxima revisão deve redesenhar conjuntamente lance principal, abertura do mezanino e chegada superior.
