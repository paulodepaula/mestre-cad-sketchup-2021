# Obra com mezanino - R08 (viga V05, C07 e vidro superior)

**Fonte unica:** `model.json` no GitHub, sincronizado pelo plugin Mestre CAD no SketchUp 2021. Nada de desenho manual.

## R08 no CAD
- V05 foi prolongada de 3m para **4m**, terminando na largura da coluna **C10**.
- **C07** vai do piso a **5,355m** para encontrar geometricamente a viga inclinada V13 e servir de **montante das esquadrias**.
- Dois planos de vidro de estudo foram acrescentados na porcao superior dos fundos, ao longo da linha recuada Y5621: `VF08_SUP_ESQ` e `VF08_SUP_DIR`. As faces podem parecer opacas no SketchUp atual: sua TAG e metadados indicam material de vidro, **sem sistema de esquadrias definido**.
- O **fechamento inferior e a porta** ainda nao foram modelados para nao bloquear o acesso.
- **Piso do mezanino 160mm**: permanece reserva geometrica. Alternativas de **placas cimenticias ESPECIFICAS para mezanino** em analise; nao se escolheu produto/espessura de placa.
- C02-C06 continuam como tubos de estudo 150x150x3mm, telhado e lote intactos. 52 elementos totais, sem dimensionamento estrutural.

Mais informacoes: [R08-VIDRO-PISO-CIMENTICIO.md](R08-VIDRO-PISO-CIMENTICIO.md).
Historico preservado: `historico/model-R07.json`.
