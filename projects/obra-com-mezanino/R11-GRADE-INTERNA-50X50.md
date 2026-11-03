# R11 - Grade 50x50 interna ao quadro de vigas

**Estudo geometrico, NAO executivo.** Fonte R10 do commit f97de556f3fedcd09da626ddc73935efb6a312e8. O rascunho R11 anteriormente produzido fora do GitHub nao foi utilizado: ele mudava pilares, identificacoes e vigas que nao faziam parte do pedido.

## Mudanca solicitada
A grade foi reposicionada **por dentro do quadro das vigas**, conforme o conceito da fotografia enviada, com tubos de secao externa 50x50mm. A imagem nao forneceu medidas, espessuras ou capacidade estrutural. A espessura da parede do metalon permanece `null` (a definir), distinta dos 3mm especificados anteriormente somente para C02-C06.

## Coordenadas e encontros
As vigas principais mantem suas coordenadas da R10, inclusive o topo Z2690. A grade ocupa **Z2640..2690**, os ultimos 50mm da altura das vigas, e se encontra com as faces internas delas.

- Quadro principal livre: X6561..9361, Y721..5521 mm.
- 12 travessas G11_MT01..12 de 2800x50x50mm, em Y971..5371 com passo de 400mm.
- Duas linhas longitudinais em X7461 e X8461, cada uma dividida em 13 trechos entre as travessas, totalizando 26 barras G11_ML. Essa divisao evita atravessar uma barra com outra no modelo. Os trechos curtos conectam-se nas laterais das travessas; **nao constituem novos apoios independentes** que reduzam automaticamente o vao de 2,80m.
- Patamar: quatro travessas G11_PT01..04, 900x50x50mm entre X9461..10361, e cinco trechos longitudinais G11_PL01_01..05 em X9911. A reserva da escada continua livre de barras novas.
- Retirados 26 perfis sobrepostos da R10, prefixos BM_ e BP_. As duas soleiras SG_ESQ/SG_DIR foram mantidas e rebaixadas.
- Solda e apenas o conceito da ligacao. Nao foram modelados ou calculados cordoes, chapas de reforco, recortes e ligacoes reais.

## Correcao necessaria de nivel
**Nao seria geometricamente correto manter simultaneamente o topo das vigas em 2690, embutir a grade nesse topo e manter uma unica placa de 25mm com acabamento em 2850.** Isso recriaria o vao de 135mm ou exigiria mudar vigas que o usuario nao pediu para levantar.

Por isso: grade e vigas terminam em **Z2690**, o piso de 25mm ocupa **Z2690..2715**, e o patamar acompanha a mesma cota. A reducao em relacao a R10 e de **135mm**. A indicacao de manter 2,85m no rascunho anterior foi corrigida; a estrutura principal nao foi alterada.

As plantas dos dois paineis de piso continuam iguais as da R10 (principal 3000x4975 e patamar 1000x1800mm). Os recortes de placas junto aos pilares e o apoio das juntas precisam de detalhe posterior.

## Vidro sem vao visual inferior
Os panos VF08_SUP_ESQ/VF08_SUP_DIR continuam no plano Y5621, com bordas superiores preservadas e somente os dois vertices inferiores rebaixados para **Z2715**. SG_ESQ e SG_DIR ocupam Z2690..2715 e Y5596..5646, tendo contato direto com a V05. O piso principal termina em Y5596, encostando geometricamente no arremate. O vidro **nao foi assumido como apoiado estruturalmente na placa cimenticia**. Calcos, gaxetas, juntas e fixacoes permanecem pendentes. A soleira direita nao se torna piso transitavel sobre a escada.

## O que foi preservado
Pilares e suas espessuras cadastradas, todas as vigas principais e de cobertura V01-V13, contorno e inclinacao do telhado, terreno, muro B-C e reserva de escada. A oficina continua 4x6m; os 5m correspondem ao total com a passarela. Nenhuma extensao, gerador, workflow, release, permissao, material ou transparencia foi modificado.

## Verificacoes geometricas
20 testes cobrem: comparacao da R10 integral; IDs e envelope; limites do importador; secao 50x50 e topo alinhado; contatos nas duas extremidades; ausencia de interpenetracao das barras novas entre si, com pilares e vigas; conexao da grade ao quadro; contato do piso e soleiras; ausencia de vao visual sob vidro; reserva da escada; formato DXF/COLLADA; determinismo e integridade do manifesto. O teste geometrico **nao e calculo estrutural** nem teste no SketchUp Desktop real.

## Pendencias de engenharia
O mezanino sera escritorio/estacao de trabalho. A malha mais distribuida NAO aprova por si so o metalon 50x50, sobretudo no vao principal de 2,80m. Antes de fabricar: definir parede e aco, calcular resistencia, flecha e vibracao, avaliar flambagem e travamentos, detalhar soldas e bases, especificar painel/apoios de juntas, recalcular escada para Z2715 e confirmar vidro, guarda-corpos e fundacoes com responsavel tecnico.
