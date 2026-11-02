# R04 - Elementos numerados e mezanino em L ate a escada

**Revisao geometrica de estudo. Sem dimensionamento estrutural e sem verificacao normativa da escada.**

## Referencial
- X=0 borda esquerda da obra, X=4000 borda direita da oficina, X=5000 fim da passarela.
- Y=0 frente/entrada; Y=6000 fundos.
- Z=2850 topo nominal do piso do mezanino, apenas hipotese.
- Terreno T01: frente A-B (10,20m) informada, mas implantacao no lote continua sem distancias transversais/recuos validados.

## Planta superior modificada
- Recuo do piso de 1m da entrada: piso principal X=1000..4000 e Y=1000..6000 mm.
- Retorno de encontro com a escada: X=0..1000 e Y=4200..6000 mm.
- Piso em L, area bruta de estudo = 3000x5000 + 1000x1800 = **16,80 m2**.
- Encontro plano na linha Y=4200: escada reservada X=100..1000, Y=0..4200, liga com faixa de patamar X=0..1000, Y=4200..6000.
- O piso representativo manteve topo Z=2850 e espessura hipotetica 160 mm (inferencia visual, nao projeto de laje).
- A escada continua SOMENTE uma reserva 900x4200 no piso terreo; nao ha degraus, alturas, patamar de chegada/sentido ou guarda-corpo calculados. A linha de encontro na planta nao comprova acesso seguro.

## Identificacao que usaremos nas conversas
Pilares **C01-C09**, vigas **V01-V12**.
| Numero | Funcao | Posicao de estudo (mm) | Codigo R03 |
|---|---|---|---|
| C01 | pilar esquerdo frontal | X0, Y0 | P_EF |
| C02 | pilar esquerdo intermediario | X0, Y2950 | P_EM |
| C03 | pilar esquerdo fundo | X0, Y5900 | P_ET |
| C04 | pilar direito frontal | X3900, Y0 | P_DF |
| C05 | pilar direito intermediario | X3900, Y2950 | P_DM |
| C06 | pilar direito fundo | X3900, Y5900 | P_DT |
| C07 | apoio frontal esquerdo mezanino | X1000, Y1000 | PM_F_E (Y2000 antes) |
| C08 | apoio de fundo esquerdo mezanino | X1000, Y5900 | PM_T_E |
| C09 | apoio frontal direito mezanino | X3900, Y1000 | PM_F_D (Y2000 antes) |
| V01 | viga longitudinal esquerda cobertura | X0, Y0..6000 | V_COB_E |
| V02 | viga longitudinal direita cobertura | X3900, Y0..6000 | V_COB_D |
| V03 | viga longitudinal esquerda do mezanino | X1000, Y1000..6000 | VM_Y1000 (Y2000 antes) |
| V04 | viga longitudinal direita do mezanino | X3900, Y1000..6000 | VM_Y3900 (Y2000 antes) |
| V05 | viga frontal do mezanino | Y1000, X1000..4000 | VM_X2000 (Y2000 antes) |
| V06 | viga de fundo do mezanino | Y5900, X1000..4000 | VM_X5900 |
| V07 | travessa inclinada de cobertura - frente | Y0..100, X0..5000 | TR1_* (6 faces) |
| V08 | travessa inclinada de cobertura - meio | Y2950..3050, X0..5000 | TR2_* (6 faces) |
| V09 | travessa inclinada de cobertura - fundo | Y5900..6000, X0..5000 | TR3_* (6 faces) |
| V10 | viga de estudo esquerda para faixa do patamar | X0, Y2950..6000 | NOVA |
| V11 | viga transversal na chegada da escada | Y4200, X0..1000 | NOVA |
| V12 | viga transversal ao fundo do patamar | Y5900, X0..1000 | NOVA |

As travessas V07-V09 ainda sao compostas por **6 faces individuais em grupos** no SketchUp 2021, identificadas por V07_, V08_ ou V09_; representam somente 3 vigas logicas.

## Validacao de consistencia geométrica
- A linha Y4200 do retorno do piso e o termino da reserva de escada coincidem.
- Nao existe piso da faixa esquerda X0..1000 antes de Y4200, preservando a reserva geometrica da escada.
- Recuo frontal do piso superior Y1000 = 1m; a cobertura NAO foi modificada.
- Piso total 16,80 m2, area principal 15,00 m2, retorno 1,80 m2.
- Colunas e vigas possuem identificacao no `model.json`, nos nomes dos grupos do SketchUp e no DXF 2D (anotacoes).
- Nao confundir etiquetas no DXF com desenho executivo.

## Pendencias importantes
1. Validar altura livre de subida da escada e geometria com degraus reais. A reserva X100..1000 Y0..4200 ainda nao significa escada conforme normas.
2. Analisar se V10, V11, V12, C07/C09 e V03/V04 sao capazes de suportar nova geometria — **nenhum elemento foi calculado**. V10 esta em X0..100 e suporta lateral por estudo, usando a linha de apoio existente; revisar interferencias com C02/C03.
3. Verificar ligações, estabilidade, protecao contra incendio, corrimao/guarda-corpo e entrada/saida.
4. Projeto de fundacoes, sondagem, implantacao e recuo do portao ainda pendentes.
5. O gerador 1.4.1 cria faces/caixas, mas nao desenha cotas executivas, degraus, patamares em detalhe ou perfis inclinados como unico objeto solido.

## Proxima revisao R05
Verificar escada real e alturas livres em corte antes de desenhar degraus ou liberar componentes para compra/fabricacao.
