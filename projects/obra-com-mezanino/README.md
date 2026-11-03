# Obra com mezanino - R11

Fonte unica: `model.json` no GitHub, sincronizado pelo plugin Mestre CAD 2021. Revisao de estudo, NAO executiva.

## Grade do piso por dentro das vigas
- Grade secundaria em tubos de dimensao externa **50 x 50 mm**, entre as faces internas das vigas existentes, com topo alinhado em **Z2690 mm**. Nao ha grade empilhada por cima das vigas.
- Ligacao soldada representada pelo encontro das barras, sem detalhamento de cordoes. Espessura de parede do tubo **a definir**; nao foi adotada automaticamente a espessura de 3mm dos pilares.
- Malha principal: 12 travessas e 26 trechos longitudinais. Patamar: 4 travessas e 5 trechos longitudinais. As intersecoes sao encontros de faces, sem sobreposicao de prismas.
- Piso e patamar de 25mm de estudo apoiados em **Z2690..2715 mm**. O piso acabado passou de **2,850 m para 2,715 m**, sem levantar nem redimensionar as vigas principais. A cota antiga era resultado da grade sobreposta.
- Vidros superiores e soleiras acompanham o novo piso, com base em **Z2715 mm**, sem vao visual inferior. Vidro sem fume; aparencia inalterada.
- Oficina **4000 x 6000 mm**, mais passarela de 1000mm. Pilares, V01-V13, telhado, muro e terreno preservados da R10.
- **101 elementos**: 47 barras novas da grade, 2 soleiras ajustadas e elementos existentes. R10 integral arquivada em `historico/model-R10.json`.

## Limites
A maior distribuicao de barras nao comprova a capacidade de tubos 50x50, especialmente nas travessas com 2,80m entre as vigas. Espessura, cargas, flecha, vibracao, soldas, estabilidade e fundacoes permanecem sem dimensionamento. A escada ainda e reserva geometrica; sua chegada precisa acompanhar Z2715. Placa e recortes junto aos pilares nao detalhados.

Documentacao: [R11-GRADE-INTERNA-50X50.md](R11-GRADE-INTERNA-50X50.md). Metodo permanente: [AGENTS.md](AGENTS.md).
