# R05 - Entrada pelos fundos, fachada recuada, piso de mezanino e pilar compartilhado

**Modelo de estudo, NAO executivo. A geometria da cobertura foi preservada integralmente da R04.**

## Implantacao e entrada
- O terreno mantem a frente A-B (rua) conforme T01; **a entrada da OFICINA agora fica nos fundos da obra**, na orientacao interna Y=6000.
- O fechamento esta no plano **Y=5000**, 1000 mm antes da borda posterior do piso e do telhado (Y6000).
- Vidros a esquerda: **X=0..1000**, plano Y5000, Z0..2400 (altura hipotetica).
- Portao a direita: **X=1000..4000**, plano Y5000, Z0..2400 (altura hipotetica).
- Faixa superior simbolica X0..4000, Z2400..2690 no mesmo plano Y5000. Os elementos sao faces sem espessura, nao esquadrias operacionais, e nao especificam tipologia/posicionamento do portao real.

## Mezanino atualizado
- Piso principal: X1000..4000, Y0..5000, topo Z2850, 15,00 m2.
- Retorno da chegada de escada: X0..1000, Y4200..5000, topo Z2850, 0,80 m2.
- Area total de estudo **15,80 m2**.
- Recuo do piso no lado da nova entrada (fundos): Y5000..6000 = 1m.
- Reserva de escada continua X100..1000 Y0..4200. Ela encontra a faixa lateral na linha Y4200; sem degraus, patamar/corrimaos e geometria de alturas verificados.

## Colunas de referencia
- **C04** coluna direita principal em X3900 Y0: tambem e referencia de apoio do mezanino.
- **C09 nao existe mais como segunda coluna.** O codigo antigo e um alias historico: C09 -> C04.
- C01..C06 sao as colunas principais, com posicoes/dimensoes visuais intocadas.
- C07 mudou de X1000/Y1000 para X1000/Y0, acompanhando a borda frontal do piso invertido.
- C08 mudou de X1000/Y5900 para X1000/Y4900, proximo a borda de fundo do mezanino (estudo).
- Total 8 colunas, mas o apoio real do mezanino e sua continuidade de vigas/ligacoes nao foi dimensionado.

## Vigas de mezanino alteradas
- V03 e V04 agora percorrem Y0..5000; V04 inicia sobre a linha da C04.
- V05 passou ao limite Y0; V06 Y4900..5000.
- V10 e V12 terminam em Y5000; V11 na chegada da escada Y4200.
- **V01 e V02 e os perfis V07, V08, V09 e a face COB_R03 NAO foram alterados em dimensao ou posicao.** A verificacao automatizada compara esses elementos com o snapshot R04.

## Checagens e limites
- Envelope continua 5000 x 6000 x 5600 mm; 44 elementos geom. (19 caixas + 25 faces).
- As duas folhas esquematicas e a faixa superior fecham em planta X0..4000 no plano Y5000, sem definir perfis, esquadrias ou espessuras.
- A altura visual Z2400 de vidros/portao e hipotese que depende de pe-direito livre real, viga da fachada, automacao e tipo de portao.
- **Revisao estrutural obrigatoria**: C04 e pilar compartilhado de dois sistemas; apoio/viga frontal e vigas longitudinais precisam de verificacao de esforcos, deformacoes, travamentos, ligacoes e fundacoes. Esta geometria nao autoriza construcao.
- O telhado da R04, inclusive o balanco direito, permanece geometrica e literalmente identico.
- Recuos legais e posicao no terreno T01 ainda pendentes. A sigla "fundos" refere-se a orientacao local Y6000 da obra, **nao** a confirmacao de proximidade com os fundos do lote de 37 m.

## Proxima revisao
Definir a altura final do portao e dos vidros, sentido da abertura, calha, paredes laterais, escada e patamar reais sem modificar a cobertura ate autorizacao expressa.
