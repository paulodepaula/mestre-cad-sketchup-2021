# R19 - correção visual da porta de enrolar vazada

A R18 continha a porta no JSON e no DAE, porém a cortina era uma única `face` sem espessura. No SketchUp isso podia ficar pouco perceptível dependendo da vista e do acabamento.

## Correção
- `P18_FOLHA` passou de face para **caixa fina de 20mm**.
- Envelope da cortina: **2750 x 20 x 2510mm**.
- Posição: X6611..9361, Y5601..5621, Z0..2510.
- Guias laterais mantidas.
- Tipo funcional permanece **porta metálica de enrolar vazada**.

A malha/perfuração continua conceitual para respeitar o limite de 150 elementos do importador. O material de grade/vazada pode ser aplicado no SketchUp e será preservado pelo comando da extensão v1.5.0.

Nenhum outro elemento do projeto foi alterado.
