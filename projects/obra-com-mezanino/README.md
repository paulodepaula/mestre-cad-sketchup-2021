# Obra com mezanino - R05 (entrada pelos fundos; estudo NAO EXECUTIVO)

A fonte geometrica e `model.json`. Arquivos DXF, DAE e manifesto sao derivados no GitHub Actions. A geometria R04 anterior esta arquivada em `historico/model-R04.json`.

## Alteracoes R05 aprovadas
- A **entrada da oficina esta nos fundos**, com fechamento do lado Y6000 **recuado para Y5000** (faixa coberta de 1m).
- Vidro esquerdo de largura 1000 mm X0..1000 e portao direito de largura 3000 mm X1000..4000, ambos alinhados em Y5000. Altura ilustrativa Z0..2400; fechamento superior simbolico Z2400..2690.
- Mezanino em L reposicionado para liberar o recuo no acesso: principal 3000 x 5000 mm (Y0..5000) + retorno de escada 1000 x 800 mm (Y4200..5000); area bruta total 15,80 m2.
- Coluna C09 absorvida por C04. Total **8 colunas** (C01..C08); os pilares principais da cobertura continuam sem modificacao de posicao/volume.
- Vigas do mezanino ajustadas ao novo piso. O encontro com a escada continua somente geometrico.

## Telhado congelado
**O telhado NAO foi alterado:** face `COB_R03`, vigas `V01`, `V02`, cascas V07, V08, V09 possuem mesma geometria da R04. Inclui balanco de 1000 mm, sem pilar na borda lateral. Teste de regressao compara R05 ao R04.

## Referencias e situacao
- C09 passa a ser alias historico de C04; usar **C04** daqui por diante.
- Dimensoes principais oficina 4000 x 6000 mm e passarela 1000 mm mantidas.
- Alturas, espessuras, apoios, vedacoes, tipo do portao, cargas, escada, fundacoes e recuos carecem de projeto tecnico e validacao por engenheiro.
- Terreno T01 possui frente A-B de 10,20 m, area estimada 382,15 m2, implantacao definitiva ainda nao posicionada.
- Documentacao de R05: [R05-ENTRADA-FUNDOS.md](R05-ENTRADA-FUNDOS.md).

## SketchUp / CadCraft
Sincronizar arquivos CAD do GitHub > Importar projeto sincronizado > Conferir grupo selecionado. A extensao importa faces e caixas como grupos editaveis, mas nao converte faces de portao em componentes funcionais.
