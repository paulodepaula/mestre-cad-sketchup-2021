# R15 - escada reta lateral compacta e corredor superior aproximado de 1m

**ESTUDO GEOMETRICO, NAO EXECUTIVO.** A escada em U da R14 foi retirada porque ocupava area excessiva da oficina e do mezanino.

## Solucao adotada
- Escada **reta lateral**, um unico lance, faixa X9461..10361mm.
- Limites Y1629..5521mm: desenvolvimento horizontal **3892mm**, sem ultrapassar a linha de C07/C10 em Y5521.
- **15 espelhos de 181mm** = desnivel total 2715mm.
- **14 pisos de 278mm**, largura nominal 900mm.
- Relacao geometrica 2h+b = **640mm**.
- O corredor/patamar superior ocupa Y621..1629 = **1008mm**, aproximadamente 1,00m.
- A chegada encontra o topo do mezanino em Z2715mm.
- C02 permanece 100x100x3mm e nao invade a faixa da escada.

## Recuperacao de area
A geometria dos paineis de piso volta a usar o MEZ_PRINCIPAL integral da R13. Somente o antigo patamar de 1,80m e reduzido para 1,008m.

| Revisao | Area geometrica de paineis do mezanino |
|---|---:|
| R13 | 16,725 m2 |
| R14 - escada U | 12,9975 m2 |
| **R15 - escada reta** | **15,933 m2** |

A R15 recupera **2,9355m2** em relacao a R14 e perde somente **0,792m2** em relacao a R13.

## Estrutura local
- V03 volta a geometria integral da R13.
- V14, V15, MEZ_FRENTE_R14, MEZ_FAIXA_R14 e todos os elementos E14 foram retirados.
- V11 foi deslocada para Y1529..1629, formando o cabecalho do corredor superior.
- A grade 50x50 do patamar foi compactada: G11_PT03, G11_PT04, G11_PL01_04 e G11_PL01_05 foram retiradas; G11_PL01_03 termina em V11.
- Restante da grade, vigas principais, pilares, vidro, telhado, terreno e muro seguem a R13.

## Limites
Os degraus, espelhos, duas longarinas e um plano de guarda sao geometria de estudo. Perfil das longarinas, chapa dos degraus, soldas/parafusos, corrimaos, guarda-corpos, largura util final, altura livre, resistencia ao fogo, acessibilidade e fundacoes nao foram dimensionados.

A geometria 181/278 gera 2h+b=640mm, mas isso **nao constitui aprovacao normativa**. O enquadramento real da escada para escritorio, seguranca contra incendio e regras locais deve ser confirmado por profissional habilitado.

Historico integral anterior: `historico/model-R14.json`.
