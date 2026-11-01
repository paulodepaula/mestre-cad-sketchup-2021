# Geração nativa SKP no GitHub - dependencia externa

O pipeline atual gera um arquivo 3D `.dae` COLLADA e o desenho 2D `.dxf`. Ambos sao artefatos reais, deterministas e versionados. SketchUp 2021 pode importar o DAE e a extensao Mestre CAD pode importar o JSON para gerar grupos, permitindo salvar `.skp` localmente.

Para produzir `.skp` **diretamente em um runner do GitHub**, precisamos solicitar acesso ao [SketchUp C SDK oficial](https://developer.trimble.com/docs/sketchup/tools/sdk/), instalar o SDK em um runner Windows/macOS permitido, compilar o conversor proprio e testar o salvamento no formato 2021.

Nao foram incluidas DLLs/headers do SDK porque a distribuicao depende das condicoes do fabricante e do acesso autorizado. Nao e correto chamar um DAE ou ZIP de SKP. Ate essa etapa estar pronta, a unica forma validada de produzir um SKP nativo e abrir os dados no SketchUp Desktop 2021 e salvar nele.

O workflow atual nao executa o SketchUp via emulacao/servidor e nao exige SketchUp no runner Linux para gerar DXF e DAE.

## Extensao 1.4.0: SKP local automatico

O SketchUp Desktop 2021 salva uma copia nativa `.skp` automaticamente ao importar o projeto sincronizado. O metodo `Sketchup::Model#save_copy` (suportado desde 2014) preserva o arquivo principal aberto. O usuario tambem pode salvar uma copia do grupo selecionado sem reimportar. Nao ha geracao de SKP no runner GitHub nem push automatico de arquivos SKP.
