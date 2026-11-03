# Obra com mezanino - R14

Fonte central: model.json no GitHub. Sincronizacao pelo plugin Mestre CAD 2021. ESTUDO GEOMETRICO, NAO EXECUTIVO.

## Escada agora representada em 3D
- Dois lances em U, 16 espelhos iguais de 169,6875 mm, 14 pisos de degraus de 300 mm e patamar intermediario a 1357,5 mm. Chegada ao mezanino mantida em 2715 mm.
- Cada lance tem 900 mm entre as faces das longarinas; envelope total de 2100 x 3100 mm. O conjunto termina em Y5521, sem ultrapassar a face C07/C10 em Y5621.
- Inclui degraus volumetricos, fechamento dos espelhos, patamar, quatro apoios, longarinas e planos de guarda. Longarinas e guardas sao faces de referencia, sem espessura ou fixacao definida. Corrimaos preensiveis e arremates continuam pendentes.
- A reserva anterior de 900 x 3200 mm nao foi tratada como uma escada pronta. A solucao em U exige abertura adicional no piso: a area geometrica dos paineis passa de 16,725 para 12,9975 m2 (reducao de 3,7275 m2, aproximadamente 3,73 m2).
- V03 foi limitada ao trecho Y621..2421; acrescentadas V14 e V15 para contornar o vazio. Grade 50x50 local recortada e compatibilizada. Essa mudanca exige RECALCULO do quadro do mezanino e das ligacoes, nao autorizacao de cortar uma estrutura em obra.
- Pilares, cobertura, terreno, muro, vidro sem fume, soleiras, cota do mezanino e implantacao 4 x 6 m preservados.
- 150 elementos, limite da extensao atual. R13 integral preservada em historico/model-R13.json.

## Validacao e limites
Testes geometricos: igualdade dos elementos preservados, dimensoes, degraus, niveis, contatos da grade, ausencia de interpenetracao de caixas novas, amostragem de altura livre, DXF/DAE e manifesto. Isso nao substitui calculo de perfis, soldas, apoios, bases, fundacoes ou verificacao normativa completa.

Detalhes e fontes: [R14-ESCADA-U-3D.md](R14-ESCADA-U-3D.md).
