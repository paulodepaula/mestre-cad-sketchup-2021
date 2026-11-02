# Obra com mezanino - R01: planta e posicionamento de estudo

**Status: REFERENCIA GEOMETRICA NAO EXECUTIVA.** `model.json` e a fonte de verdade para o gerador e a sincronizacao da extensao Mestre CAD 2021.

## Medidas e eixos

- X cresce para a direita, de frente para a oficina. Y cresce da frente para o fundo. Z e elevacao acima do piso de referencia.
- **Definidos pelo usuario:** oficina principal 4.000 x 6.000 mm; faixa/passarela a direita com largura de 1.000 mm; terreno com 10.000 mm de frente (nao representado no envelope); oficina terrea e deposito/ferramentas; mezanino destinado a escritorio.
- **Proposta geometrica provisoria:** faixa direita acompanha 6.000 mm de profundidade; mezanino de 3.000 x 4.000 mm (12 m2) em X=1.000..4.000, Y=2.000..6.000; nivel Z=2.850 mm; reserva da escada de 900 x 4.200 mm na esquerda, X=0..900, Y=0..4.200.
- **Envelope do ARQUIVO:** X=5.000, Y=6.000, Z=2.850 mm. Z indica **somente a cota mais alta REPRESENTADA**, NAO a altura total da edificacao.
- A cobertura, pilares e fundacoes de R00 foram retirados do **modelo ativo**, porque nao estavam dimensionados. O arquivo original foi preservado em `historico/model-R00.json`.
- As faces de piso, passarela, reserva de escada e mezanino sao referencias SEM espessura, suporte estrutural, vãos ou verificacao de cargas.
- A face do mezanino e uma hipotese de localizacao, nao uma laje executiva: o acesso no topo da escada, patamar e pe-direito precisam ser resolvidos antes do detalhamento.
- O espaco de pe-direito duplo e a area de impressao 3D precisam ser compatibilizados: impressoras e armarios exigem piso estrutural, ventilacao e circulacao; nao ficam apoiados no vazio.
- Sem alteracao ou aprovacao de dimensoes estruturais. O nivel de R00 (3.420 mm) e seus pilares sao apenas referencia historica.

## Arquivos e operacao

Alteracoes em `model.json` na branch `main` acionam GitHub Actions, que gera `cadcraft/planta.dxf`, `cadcraft/elevacoes.dxf`, `sketchup/modelo.dae` e `manifest.json`. Verifique sucesso do workflow e integridade do manifesto antes de sincronizar.

SketchUp 2021: Extensoes > Mestre CAD 2021 > Sincronizar arquivos CAD do GitHub; Importar projeto sincronizado; Conferir grupo selecionado; Salvar copia SKP do projeto sincronizado. O SKP permanece local.

Detalhes e pendencias: [R01-PLANTA-E-MEZANINO.md](R01-PLANTA-E-MEZANINO.md).

## Levantamento adicional: interferencia do portao

O proprietario informou que o portao deslizante para a direita ocupa **300 mm** do lado interno do muro frontal, ate sua extremidade mais interna incluindo motor (portao totalmente aberto). Esse valor esta registrado em `model.json > levantamento_campo_mm` e **nao e o recuo final da edificacao**. A geometria e seu envelope continuam locais (X=0 a esquerda da oficina, Y=0 na fachada proposta), sem deslocamento no terreno; faltam folga de manutencao, posicao lateral e verificacao de afastamentos obrigatorios. Consulte `R01-PLANTA-E-MEZANINO.md`.
