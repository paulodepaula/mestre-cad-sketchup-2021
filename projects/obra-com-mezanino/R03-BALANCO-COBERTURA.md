# R03 - Proposta de balanco na cobertura, com passarela direita sem pilares

**ESTUDO GEOMETRICO, NAO PROJETO EXECUTIVO.** Fonte geometrica anterior arquivada em `historico/model-R02.json`.

## Decisao arquitetonica
- Construcao: X0..4000, Y0..6000 mm.
- Passarela coberta lateral direita: X4000..5000, Y0..6000 mm (6 m de comprimento propostos).
- Extremo da cobertura em X5000; inicio do balanco em X4000: 1000 mm nominais.
- Removidos `P_PF`, `P_PM`, `P_PT` e `V_COB_P` (hipoteses R02). Nenhum pilar externo na passarela.
- Mantidos os seis pilares principais de estudo em X0 e X3900, Y0,2950,5900; 100x100 mm so marcador e nao tamanho projetado.

## Representacao no gerador
- 3 travessas inclinadas: Y0..100, Y2950..3050, Y5900..6000. Cada travessa usa seis faces, pois o Mestre CAD 2021 v1.4.1 aceita apenas `caixa` e `face`.
- Faces formam uma casca geometrica de estudo, nao um perfil ou ligacao fabricavel.
- Face superior vai de Z5585 em X0 a Z5335 em X5000; face inferior 175 mm abaixo. Secoes de 100/175 mm sao **apenas ilustrativas**.
- Cobertura mantida como face sem espessura de Z5600 (X0) a Z5350 (X5000), caimento hipotetico 5%.
- Vigas longitudinais internas em X0 e X3900 permanecem como volumes de estudo.
- Envelope: X5000 / Y6000 / Z5600; 38 elementos: 16 caixas e 22 faces.

## Alertas obrigatorios
- Nao foi calculada resistencia ao momento, cisalhamento, flecha, arrancamento por vento, rigidez do engaste, travamento lateral nem ancoragens ou estabilidade do conjunto.
- O fato de existir uma travessa na imagem nao prova que seja seguro deixar 1 m em balanco. Engenharia estrutural e validacao do projeto sao obrigatorias.
- Sem detalhar calhas, telhas, dreno, esquadrias, fundacao, recuos e escada; outras dimensoes anteriores nao foram homologadas.
- Vao livre de passarela, espessuras de acabamentos e acessibilidade requerem dimensionamento futuro.

## Conferencias da R03
- Extremidade externa sem pilar: nenhum marcador estrutural com origem X4900.
- Travessas terminam X5000. Linha de limite da oficina X4000 e balanco 1000 mm.
- Mezanino, reserva de escada, area de oficina e profundidade mantidos.
- A imagem original e apenas referencia arquitetonica, nao desenho executivo.
