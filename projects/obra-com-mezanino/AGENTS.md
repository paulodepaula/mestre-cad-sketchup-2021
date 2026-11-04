# AGENTS.md - Contrato permanente deste projeto

## Fonte da verdade
- Ler tambem `CONTEXTO-OPERACIONAL.md` antes de qualquer alteracao; ele fixa convencao espacial, fluxo e incidentes conhecidos.
- O usuario determinou em 2026-11-02: **todos os desenhos e arquivos do projeto devem ser produzidos DIRETAMENTE no GitHub** `paulodepaula/mestre-cad-sketchup-2021`, pasta `projects/obra-com-mezanino`.
- **NAO instruir o usuario a desenhar, modelar, importar DXF manualmente, criar linhas ou executar scripts manualmente no SketchUp ou no CadCraft.** Essa orientacao substitui procedimentos manuais anteriores.
- Para cada alteracao pedida: buscar ultimo commit, editar diretamente `model.json` e os arquivos de projeto necessarios, publicar por commit na `main`, acompanhar testes e geracao de `planta.dxf`, `elevacoes.dxf`, `modelo.dae` e `manifest.json`.
- **SketchUp**: o usuario apenas usa o plugin Mestre CAD 2021 para **sincronizar o projeto do GitHub e importar o modelo sincronizado**. SKP local nao e enviado automaticamente ao Git. **CadCraft** usa DXF do mesmo projeto.
- Ao responder: informe revisao, resultado do CI, resumo das mudancas e links ao GitHub; **nao fornecer passo a passo operacional salvo pedido explicito**.
- Preservar revisoes no historico. Referenciar membros ativos C01-C08, C10 e V01-V13, com C09 como alias historico de C04; alteracoes de vigas/apoios devem registrar posicao em mm. Alteracoes na superficie/contorno/caimento do telhado exigem autorizacao expressa.
- Diferenciar medidas do KMZ estimativo (T01) de medidas aferidas em campo. Frente do lote A-B, fundos C-D, muro direito B-C com altura informada 4800mm.
- Recuo de 300mm do muro da rua para o portao, entrada funcional da oficina orientada para C-D, cobertura encostada visualmente em B-C somente como estudo legalmente nao aprovado, faixa de 1m voltada para esquerda/centro do terreno.
- Nao declarar o modelo seguro ou projeto executivo sem calculo e responsabilidade tecnica.

Este arquivo registra o metodo de trabalho para todos os proximos agentes e sessoes neste repositorio.
