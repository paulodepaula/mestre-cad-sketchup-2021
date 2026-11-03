# Obra com mezanino - R12

Fonte unica: `model.json` no GitHub, sincronizado pelo plugin Mestre CAD 2021. Revisao de estudo, NAO executiva.

## Escada limitada a coluna do mezanino
- A reserva `ESCADA_RES` agora termina na **face externa da C07, alinhada a C10 e ao vidro: Y5621mm**. Antes terminava em Y6621.
- Espaco de estudo: **900 x 3200mm**, no intervalo X9461..10361 e Y2421..5621. A extremidade de acesso recua 1000mm; a chegada ao patamar em Y2421 permanece.
- O piso acabado do mezanino continua em **Z2715mm**. A escada ainda e somente uma reserva em planta, sem degraus dimensionados; nao e uma escada pronta para fabricar.
- Interferencia preexistente a resolver: **C02 ocupa 50mm da faixa nominal**, deixando 850mm localmente antes de corrimaos. Nao se moveu nenhum pilar nesta revisao.
- Todos os demais **100 elementos da R11** preservados, inclusive grade interna 50x50, piso, patamar, vidros/soleiras, V01-V13, colunas, cobertura, terreno e muro. **101 elementos** no total.
- Oficina 4000x6000mm mais passarela de 1000mm. Vidro sem fume. Nenhuma alteracao da extensao ou dos workflows.

## Historico e limites
R11 integral arquivada em `historico/model-R11.json`. Grade 50x50 e espessura de piso 25mm permanecem hipoteses sem verificacao estrutural. Escada, guardas, soldas, estabilidade, fundacoes e recuos requerem projeto tecnico.

Detalhe da mudanca: [R12-ESCADA-LIMITE-C07.md](R12-ESCADA-LIMITE-C07.md). Grade anterior: [R11-GRADE-INTERNA-50X50.md](R11-GRADE-INTERNA-50X50.md). Metodo permanente: [AGENTS.md](AGENTS.md).
