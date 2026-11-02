# R09 - Correcao do piso para liberar o encontro com os paineis de vidro

**Revisao para importacao sincronizada no SketchUp 2021. NAO EXECUTIVA.**

## Alteracao realizada no CAD
- Piso principal do mezanino `MEZ_PRINCIPAL`: antes origem (6461,621,2690) mm e volume (3000,5000,160) mm; agora origem **(6461,621,2825)** mm, dimensoes externas **(3000,4975,25)** mm.
- Patamar `MEZ_PATAMAR`: antes origem (9461,621,2690) mm e volume (1000,1800,160) mm; agora origem **(9461,621,2825)** mm e volume **(1000,1800,25)** mm.
- **Cota superior acabada mantida Z=2850mm.** O modelo foi corrigido visualmente de 160mm para uma **chapa de 25mm**, somente como estudo de placa de piso.
- Os paineis do vidro `VF08_SUP_ESQ` e `VF08_SUP_DIR` estao no plano **Y=5621mm**, iniciando em **Z=2850mm**. O piso principal agora termina em **Y=5596mm**, portanto com **25mm de folga geométrica antes do plano de vidro**. Nenhum painel invade o volume modelado do piso. Esta folga **exige posterior arremate e suporte da esquadria; nao deixar vao aberto em obra**.
- **C04/C07/C10, V05, V13, mezanino em planta e lote permanecem** nas mesmas posicoes, sem alteracao estrutural.

## Restricao importante: chapa nao apoiada nas vigas atuais
As vigas do mezanino V03/V04/V05 continuam com topo Z=2690mm. A chapa visual com 25mm tem face inferior Z=2825mm: **135mm sem subestrutura desenhada entre viga e painel**.

**A chapa so representa o acabamento/placa do futuro sistema de piso.** Nao executar assim e nao assumir que placa de 25mm vence o vao do mezanino. O projeto precisa de travessas metalicas secundarias ou sistema especifico para fechar a diferenca de nivel e dar apoio a chapa, com espacamento, espessura e carga calculados. A composicao final pode ter espessura global maior que 25mm, mas seus componentes nao devem invadir a zona da esquadria.

O material final ainda nao foi escolhido: placas cimenticias comuns de vedacao nao sao automaticamente adequadas para piso. Exigir placa explicitamente recomendada para piso/mezanino, ficha de cargas, fixacoes, resistencia a umidade e projeto estrutural com ART.

## Historico
- R08 arquivada em `historico/model-R08.json`.
- Geometria atual: `model.json` R09.
- A placa de piso continua apenas **hipotese visual 25mm**, nao secao executiva. Nenhuma porta ou parede inferior foi modificada.
