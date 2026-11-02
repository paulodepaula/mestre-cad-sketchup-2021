# R07 - pilares tubulares 150 x 150 x 3 mm para estudo

**Revisao R07 incorporada ao modelo principal para sincronizacao com SketchUp/CadCraft.**
Esta revisao e um **estudo geometrico**; espessura de parede 3 mm foi definida pelo proprietario, mas nao foi calculada nem aprovada como resistente.

| Pilar | Origem XYZ (mm) | Largura x profundidade x altura (mm) | Parede tubular |
|---|---|---|---|
| C02 | 10311, 3571, 0 | 150 x 150 x 5420 | 3 mm |
| C03 | 10311, 621, 0 | 150 x 150 x 5420 | 3 mm |
| C04 | 6461, 5521, 0 | 150 x 150 x 5225 | 3 mm |
| C05 | 6461, 3571, 0 | 150 x 150 x 5225 | 3 mm |
| C06 | 6461, 621, 0 | 150 x 150 x 5225 | 3 mm |

## Diretrizes de preservacao
- **C02/C03**: secao cresce para dentro do lote, mantendo face de direita X10461 igual a linha B-C. Nao avancam alem da divisa na geometria aproximada.
- **C04/C05/C06**: mantidas com face esquerda X6461, expandindo a secao 50 mm para a direita, dentro da oficina, sem entrar na faixa da passarela do lado esquerdo.
- Em Y os apoios crescem 50 mm na direcao positiva, deslocando eixos centrais cerca de 25 mm. **Verificar em calculo e detalhamento real o encontro com vigas do mezanino e do telhado**, sem presumir continuidade ou ligacao validada.
- **C01, C07, C08 e C10**, as vigas V01-V13, o telhado, o mezanino e o terreno **nao foram alterados**.
- A atual extensao SketchUp suporta somente `caixa` e `face`; por isso os pilares aparecem como **prismas exteriores macicos na visualizacao**, apesar da especificacao cadastrada ser um **TUBO QUADRADO VAZADO** de parede 3 mm. **Nao comprar barra macica**.
- Status normativo: perfil, composicao do aco, rigidez, flambagem, estabilidade lateral, travamentos, ligacoes e base/fundacoes nao verificados. Espessura 3 mm NAO significa capacidade garantida. Projeto estrutural com ART exigido.

## Consulta de precos, 02/11/2026
Em Vilhena/RO, fornecedores Vanzin Ferro e Aco, NSA Ferro e Aco e Minasferro foram encontrados, mas **nao foi publicado um preco local para as vigas**. Referencias nacionais publicas, SEM FRETE:

| Perfil de referencia (NÃO igual ao modelo 100x175mm) | Barra 6 m |
|---|---:|
| Viga W150 x 13kg/m | R$ 899,66 (Hiperferro) |
| Viga W200 x 15kg/m | R$ 1.033,70 (Hiperferro) |
| Perfil U enrijecido 150x60x20mm t=3mm | R$ 336,38 (Hiperferro) |
| Tubo quadrado 150x150mm t=3mm | R$ 1.102,25 (Dominik Metalcenter) |

Fontes:
- https://hiperferro.com.br/barras-e-perfis/perfil-estr-w.html
- https://hiperferro.com.br/chapas-tubos-e-perfilados/perfis-de-chapa-virada/perfil-udc-enrijecido/perfil-u-enrij.html
- https://acos.dominik.com.br/product/tubo-quadrado-preto-150-x-150-3-00mm-f-q-85-67kg-m-pt/
- https://www.vanzin.ind.br/product-category/industrial-estrutural-e-serralheria/

**A geometria de estudo das vigas (100x175mm e 100x180mm) nao define perfil comercial, tipo de aco nem espessura.** A cotacao final depende de definir o perfil por calculo, comprimento e corte, entrega em Vilhena, soldagem, pintura e montagem.
