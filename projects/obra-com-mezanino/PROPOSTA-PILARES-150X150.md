# Estudo de alternativa estrutural - pilares 150 x 150 mm

**Status:** hipotese solicitada pelo proprietario em 2026-11-02. **Nao autorizada para fabricacao nem incorporada na geometria ativa R06.**

## Objetivo
Avaliar a substituicao da secao representativa de **100 x 100 mm** por **150 x 150 mm** nas colunas **C02, C03, C04, C05, C06**, mantendo, por ora, a revisao R06 pronta para sincronizacao sem alteracao.

## Coordenadas atuais - modelo R06 em milimetros
| Pilar | Origem X,Y,Z (mm) | Secao geometrica atual (mm) | Altura (mm) | Proposta de estudo |
|---|---|---|---|---|
| C02 | 10361, 3571, 0 | 100 x 100 | 5420 | 150 x 150 mm, espessura a definir |
| C03 | 10361, 621, 0 | 100 x 100 | 5420 | 150 x 150 mm, espessura a definir |
| C04 | 6461, 5521, 0 | 100 x 100 | 5225 | 150 x 150 mm, espessura a definir |
| C05 | 6461, 3571, 0 | 100 x 100 | 5225 | 150 x 150 mm, espessura a definir |
| C06 | 6461, 621, 0 | 100 x 100 | 5225 | 150 x 150 mm, espessura a definir |

A dimensao 150 x 150 mm significa **envelope externo** do pilar; nao define a espessura t da parede do tubo, tipo de perfil, qualidade do aco, peso linear, resistencia ou capacidade de carga. O crescimento de 50% da largura aparente NAO permite concluir crescimento fixo de capacidade.

## Restricoes de geometria
- C02 e C03 atualmente ocupam X=10361..10461mm. A face direita X=10461mm coincide com a **linha de referencia do muro B-C**. Aumentar a largura mantendo a origem atual projetaria 50 mm alem desta linha, o que **nao pode ser feito**.
- Uma **alternativa geometrica, sem aprovacao**, seria deslocar as origens X de C02 e C03 para 10311 mm, mantendo a face direita em X=10461 e desenvolvendo 150mm para o interior. E preciso conferir as ligacoes com V01, V10, outros elementos e o afastamento legal real.
- C04, C05 e C06 estao na linha X=6461..6561mm. Expandir para 150mm deve preservar a referencia do vao/face escolhida, sem deixar a coluna atravessar a passarela de 1m ou interferir indevidamente nas vigas do mezanino V04/V05/V06 e cobertura V02.
- Se for adotado eixo constante das colunas, a expansao muda cada face de uma secao 100 para 150 mm em **25 mm para cada lado**; isso exige verificar interferencias, bases e ligações.
- A viga V13 com C04/C10 e a alternativa de pendural da C07 **ainda nao foram dimensionadas para o peso/cargas do mezanino**. C02 e C03 podem receber reacoes diferentes de C04-C06: a reparticao depende da rigidez de vigas, laje, apoios e ligacoes. Nao presumir que as cinco colunas recebem cargas iguais.

## Verificacoes de engenharia antes de decidir espessura e secao
1. Definir **destinacao e sobrecarga do mezanino**: uso como escritorio, manutencao, estoque leve/pesado, equipamentos e cargas concentradas; levantamento das cargas permanentes.
2. Definir **perfil, espessura, classe do aco e processo de fabricacao**: pilar tubular 150x150xt nao e equivalente a pilar macico.
3. Calcular **compressao, flambagem global/local, flexo-compressao, deslocamentos laterais, estabilidade do conjunto e contraventamentos** considerando alturas e travamentos efetivos.
4. Calcular **vigas do mezanino e cobertura, vento, bases, chumbadores, fundacoes e ligacoes**. Nao supor apoio estrutural no muro vizinho B-C.
5. Projetar conforme a ABNT NBR 8800:2024 (para aco estrutural conforme escopo; edicao e erratas vigentes a verificar), ABNT NBR 14762:2010 se perfis formados a frio, ABNT NBR 6120 para acoes e ABNT NBR 6123 para vento. Exigir verificacao e ART de profissional habilitado.

## Decisao registrada
- **Propor para analise estrutural** pilares externos 150 x 150 mm em C02, C03, C04, C05 e C06.
- **Nao trocar** a geometria do `model.json` apenas porque o usuario disse "estou pensando". Dimensoes finais, posicoes de faces e espessuras dependem de decisao e calculo.
- Preservar sem alteracoes C01, C07, C08, C10, V13, o telhado, a cobertura e o terreno nesta rodada.
- Depois que a alternativa for escolhida para modelagem de estudo, publicar nova revisao no GitHub e sincronizar pelo plugin; sem desenho manual.
