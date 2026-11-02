# Obra com mezanino - R04 (estudo geometrico, NAO EXECUTIVO)

A fonte principal e `model.json`; o GitHub Actions gera DXF, DAE e manifesto. `historico/model-R03.json` preserva a revisao anterior.

## R04
- Colunas numeradas **C01-C09** e vigas **V01-V12**, como nomes de grupos no SketchUp e textos no DXF (travessas V07-V09 divididas em seis faces por viga).
- Mezanino principal com recuo frontal de 1000 mm (X1000..4000, Y1000..6000) e retorno de chegada a escada (X0..1000, Y4200..6000), area bruta hipotetica 16,8m2.
- Escada ainda reserva X100..1000 Y0..4200, chegada geometricamente alinhada a Y4200.
- Cobertura mantida em balanco de 1000mm, livre de pilares na extremidade direita.
- Encontro piso/escada, apoios e alturas **nao validam seguranca nem dimensionamento estrutural**.
- Dimensoes da oficina 4000x6000mm e passarela direita 1000mm mantidas. Posicao no terreno T01 ainda pendente.
- Projeto geotecnico e fundacoes ainda pendentes.

Detalhes e legendas em [R04-REFERENCIAS-MEZANINO.md](R04-REFERENCIAS-MEZANINO.md).

## Uso
SketchUp 2021 > Mestre CAD 2021 > Sincronizar arquivos CAD do GitHub > Importar projeto sincronizado > Conferir grupo selecionado. O SKP fica local. Nao confundir C01, V01 etc. com perfis ou secoes projetadas.

## Estado apos rollback de R05

- **Geometria ativa restaurada para R04** por solicitacao do proprietario. Modificacoes R05 (fechamento em Y5000, vidro/portao, fusao C09 com C04 e inversao do mezanino) nao fazem parte do modelo ativo.
- O estudo desfeito foi preservado no historico em `historico/model-R05-desfeito.json` e em `R05-ENTRADA-FUNDOS.md`, marcado como CANCELADO.
- **Frente da RUA no terreno T01**: A-B (10,20 m); fundos do TERRENO: C-D (10,47 m); lateral direita olhando da rua: B-C (37,02 m).
- A palavra frente/fundos da **oficina** deve ser definida separadamente da frente/fundos do terreno antes de fazer qualquer fachada, alinhamento, deslocamento ou nova implantacao.
