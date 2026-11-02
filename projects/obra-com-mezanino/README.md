# Obra com mezanino - R09 (piso liberado para esquadrias de vidro)

Fonte de verdade: `model.json` no GitHub. SketchUp 2021 apenas sincroniza/importa pelo plugin Mestre CAD, sem desenho manual.

## Correcao R09
- **MEZ_PRINCIPAL** e **MEZ_PATAMAR** reduzidos visualmente de **160mm para 25mm** como estudo de placa cimenticia para piso, **sem escolha final do material**.
- Topo do piso permanece em **Z=2850mm**, conservando a chegada da escada e nivel dos paineis de vidro.
- Borda do piso principal recuada ate **Y=5596mm**, criando **25mm de folga** em relacao aos vidros superiores `VF08_SUP_ESQ` e `VF08_SUP_DIR` em Y5621mm.
- As vigas existentes terminam em Z2690mm, portanto **faltam 135mm de subestrutura de apoio nao modelada**. A R09 nao define piso executavel nem autoriza placa sem travessas.
- V05, C07, vidro superior, telhado, terreno e as outras geometrias **inalterados**.
- 52 elementos no modelo principal, revisao R08 arquivada.
- Detalhe: [R09-CORRECAO-PISO-VIDRO.md](R09-CORRECAO-PISO-VIDRO.md).

**AVISO:** espessura visual 25mm NAO equivale a especificacao estrutural ou a um produto escolhido; fechamento da folga junto a esquadria exige detalhe tecnico.
