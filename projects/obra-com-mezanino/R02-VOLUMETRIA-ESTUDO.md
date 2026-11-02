# Obra com mezanino - R02 volumetria dimensional de ESTUDO

**NAO E PROJETO EXECUTIVO.** Elementos volumetricos nao sao dimensionamento de aco, laje, contraventamento, fundacoes ou cobertura. A revisao R01 esta arquivada em `historico/model-R01.json`.

## Geometria mantida
- Oficina X=0..4000, Y=0..6000 mm, area 24 m2 (confirmados como dimensao de projeto).
- Passarela X=4000..5000, Y=0..6000 mm (largura 1000 definida; comprimento proposto).
- Mezanino hipotetico X=1000..4000, Y=2000..6000, topo Z=2850 mm. 12 m2.
- Reserva ESCADA_RES 900 x 4200 mm; **nao ha escada executiva modelada nem patamar validado**.
- Portao desliza a direita; avanco de 300 mm para dentro do muro frontal informado. **Nao e recuo definitivo**.
- Coordenadas X direita, Y fundo, Z altura em mm; envelope da maquete de X=5000, Y=6000, Z=5600.

## Elementos adicionados, APENAS para visualizar posicoes
- 9 marcadores de pilares de **100x100 mm ilustrativos**, tres eixos de largura e tres linhas em profundidade; altura atinge base das vigas de cobertura. **Nao representam perfis aprovados**.
- 3 marcadores adicionais de apoio de mezanino de 100x100 mm, nao dimensionados.
- 3 volumes de vigas longitudinais da cobertura representadas por caixas de 100x175 mm.
- 4 volumes de vigas do mezanino representadas por caixas de 100x180 mm.
- Laje do mezanino representada por caixa de 160 mm de espessura ate o topo Z=2850. **Nao define solucao construtiva nem peso proprio**.
- Plano de cobertura sem espessura, com caimento ilustrativo de 5% da esquerda para a direita, altura Z=5600 em X0 e Z=5350 em X5000 (queda nominal de 250 mm).
- Passeio lateral direito com 1000 mm de largura bruta; pilares de 100 mm na borda externa restringem a largura livre geometrica a **900 mm**, ainda nao verificada para acessibilidade/circulacao.

## Alertas de coerencia e engenharia
1. O volume da cobertura possui pendente X; faltam travessas de suporte, fixacoes, calha, tubo de queda e verificacao da inclinacao minima do fabricante.
2. Pe-direito terreo livre proximo ao mezanino = 2690 mm (Z0 a face inferior do piso representado), sem acabamentos ou vigas adicionais. Mezanino tem somente altura em relacao ao plano de cobertura: no lado direito da oficina, caimento da cobertura torna Z aprox. 5400 mm, menos 2850 mm = 2550 mm brutos; **nao e pe-direito livre final**.
3. A escada R01 termina ao lado do mezanino com uma lacuna horizontal nominal de 100 mm. Falta patamar de transicao e calculo de espelhos/pisos e circulacao segura.
4. O modelo usa um quadro de marcos e referencia visual, nao verifica estabilidade global, flechas, cargas da oficina, estoque, vento ou mezanino. **Nao utilizar quaisquer seções ou alturas de marcadores para compra, corte ou execucao.**
5. Sem posicao definitiva em terreno, afastamento regulamentar, distancias a muro e portao; sem sondagem/fundacao.
6. O gerador 1.4.1 aceita somente `face` e `caixa`. Vigas inclinadas reais e estrutura de telhado, escada parametrica, ligações, portas e esquadrias dependem de evolucao posterior, desenhos externos ou modelagem local.

## Proxima revisao R03
- Validar implantacao, pe-direito livre de cada pavimento e geometria de acesso do patamar.
- Definir e dimensionar escada, fechamento, esquadrias, portao de enrolar e circulacao de oficina.
- Somente apos validacao profissional estrutural adotar seções e ligacoes.
