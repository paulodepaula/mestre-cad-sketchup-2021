# R06 - Uniao C04/C09, novo apoio C10 e viga V13

**Revisao de estudo geométrico publicada para SketchUp 2021 via GitHub, NAO executiva.**

## Colunas
- **C04** foi movida da origem global [6461,6521,0] para [6461,5521,0], isto e, a **posicao antes ocupada por C09**. Passou a ser o apoio unico do mezanino e da cobertura neste eixo, 100x100mm ilustrativo, com **altura 5225mm ate a base da viga de telhado V02**.
- **C09 removida** como segundo pilar; fica somente como referencia historica/alias para C04.
- **C10 nova**, para a direita olhando a rua no terreno, junto ao muro B-C (sem utiliza-lo estruturalmente): origem [10361,5521,0], volume de estudo 100x100x5420mm. Seu topo encontra a base da viga longitudinal de telhado V01.
- C04 e C10 agora compartilham a linha Y5521, separadas por eixo em X3900mm aproximadamente, com 100mm de secao nominal.

## Viga V13
- **V13** nova viga transversal superior entre C04 e C10, Y5521..5621, ao longo X6461..10461 (projecao horizontal 4m).
- Inclui seis faces em grupos `V13_SIDEA`, `V13_SIDEB`, `V13_TOP`, `V13_BOTTOM`, `V13_ENDL`, `V13_ENDR`, exatamente como a convencao anterior das travessas.
- **Inclinação acompanhando o caimento existente da cobertura**: topo em X6461/Z5385 e X10461/Z5585; fundo em X6461/Z5210 e X10461/Z5410. Altura aparente 175mm de estudo.
- Apoios tocam a zona inferior da nova travessa com pequena sobreposicao de desenho (nao representa detalhe construtivo).
- A superfície existente `COB_R03`, vigas longitudinais V01/V02 e travessas V07-V09 **nao foram modificadas**. Inserir V13 adiciona apoio sem alterar inclinacao ou contorno da cobertura.

## Terreno / situacao
- `T01_TERRENO` ~382,15m2 e `MURO_BC` 4800mm intactos.
- Oficina 4x6m, passarela 1m a esquerda e recuo do portao 300mm mantidos conforme I01.
- **50 grupos** ao sincronizar: 44 da R05, menos C09, mais C10 e seis faces da V13.
- Colunas ativas: C01-C08 e C10 (nove ao todo); C09 se torna nome historico somente.
- Geometria anterior preservada em `historico/model-R05.json`.
- Perfis, momentos, continuidade de apoio da cobertura, flecha, cargas, fixacoes e fundacoes ainda precisam ser calculados e aprovados com ART por engenheiro habilitado. Nenhum muro vizinho pode receber cargas da construcao.

## Operacao
Mudancas sao publicadas exclusivamente via GitHub e ficam disponiveis para sincronizacao pelo plugin Mestre CAD SketchUp 2021. Sem desenho manual.
