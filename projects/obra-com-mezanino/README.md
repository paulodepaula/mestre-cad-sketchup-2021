# Obra com mezanino - R05 (terreno e muro no modelo sincronizado)

**Fonte unica**: `model.json` no GitHub. O SketchUp 2021 apenas sincroniza e importa; nenhuma modelagem manual faz parte do fluxo.

## Conteudo R05
- Terreno T01 completo (contorno A-B-C-D do KMZ), muro lateral direito **B-C de 4800mm de altura** (face sem espessura).
- Oficina 4x6m e passarela 1m no referencial do terreno: **oficina do lado direito junto ao muro B-C, passarela de 1m a esquerda**, entrada funcional para os fundos C-D.
- Espaco frontal nominal 300mm no canto direito junto ao portao. Alinhamento BC sem afastamento so como estudo; checar lei e calha.
- Todos os **42 elementos da R04** preservados por rotacao de 180 graus e translacao, mantendo vigas, colunas, mezanino e geometria relativa do telhado.
- **44 grupos no modelo** (42 da oficina + `T01_TERRENO` + `MURO_BC`). Envelope do terreno/projeto: X10461 Y37341 Z5600mm.
- O novo R05 de implantacao e distinto da **R05 antiga de fachada, que permanece desfeita**.

Mais detalhes: [R05-TERRENO-MURO.md](R05-TERRENO-MURO.md). Metodo obrigatorio para proximas sessoes: [AGENTS.md](AGENTS.md).

## Operacao
Nao enviar passo a passo de modelagem: **todas as alteracoes sao feitas no GitHub**, e o usuario apenas sincroniza e importa o projeto pelo plugin do SketchUp. CadCraft recebe os DXFs gerados pelo GitHub Actions. Arquivos SKP permanecem locais.
