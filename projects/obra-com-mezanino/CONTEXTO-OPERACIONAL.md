# CONTEXTO OPERACIONAL - OBRA COM MEZANINO

Atualizado em 2026-11-04. Este arquivo e referencia permanente para novas sessoes e agentes.

## 1. Fonte da verdade
- Repositorio: `paulodepaula/mestre-cad-sketchup-2021`.
- Projeto: `projects/obra-com-mezanino`.
- Geometria central: `model.json`.
- Derivados: `cadcraft/planta.dxf`, `cadcraft/elevacoes.dxf`, `sketchup/modelo.dae`, `manifest.json`.
- O SKP permanece local; o plugin Mestre CAD 2021 sincroniza/importa o projeto do GitHub.

## 2. Fluxo obrigatorio
1. Ler `AGENTS.md`, este contexto e o `model.json` atual.
2. Alterar somente os elementos solicitados.
3. Traduzir termos espaciais para coordenadas antes de editar.
4. Atualizar testes junto com mudancas geometricas.
5. Publicar na `main`.
6. Acompanhar GitHub Actions.
7. Somente liberar sincronizacao no SketchUp apos CI `SUCCESS` e regeneracao do DAE/DXF/manifesto.

## 3. Convencao espacial definitiva
Sempre considerar uma pessoa NA RUA olhando PARA DENTRO do terreno:
- FRENTE = rua / A-B = menor Y = direcao -Y.
- FUNDOS = C-D = maior Y = direcao +Y.
- DIREITA = lado direito de quem olha da rua = maior X = direcao +X.
- ESQUERDA = lado esquerdo de quem olha da rua = menor X = direcao -X.
- Parede direita da oficina: aproximadamente X=10461.
- Passarela de 1m: lado esquerdo da oficina.
- Oficina local: aproximadamente X=6461..10461 e Y=621..6621.

Regra curta: `FRENTE=-Y | FUNDOS=+Y | DIREITA=+X | ESQUERDA=-X`.

## 4. Dimensoes e referencias
- Oficina: 4000 x 6000 mm.
- Passarela lateral: 1000 mm.
- Piso superior de estudo: topo aproximadamente Z=2715 mm.
- Escada estudada: largura nominal 900 mm; 15 espelhos de aproximadamente 181 mm; 14 pisos.
- Lance principal historico: 11 pisos de aproximadamente 278 mm.
- Trecho curto historico: 3 pisos de aproximadamente 333 mm.

## 5. Decisoes permanentes
- Nao gerar placas solares nem trilhos: o usuario usara modelo proprio.
- Nao alterar geometria do telhado sem autorizacao expressa.
- Preservar porta de enrolar, painel de madeira, passarela, pilares e vigas nao envolvidos na solicitacao.
- Alteracoes devem ser cirurgicas; nao reconstruir setores adjacentes sem necessidade.
- Nao declarar o estudo como projeto executivo ou estruturalmente seguro sem calculo e responsabilidade tecnica.

## 6. Escada - intencao atual
A configuracao a desenvolver deve obedecer:
- lance/chegada superior junto ao lado DIREITO da oficina;
- terminação superior voltada para os FUNDOS, portanto em direcao +Y;
- corredor superior livre de aproximadamente 1000 mm no lado OPOSTO, portanto a ESQUERDA da escada;
- abertura, patamar e piso do mezanino devem acompanhar essa orientacao;
- a R27 registrou incorretamente Y baixo como "fundos" e nao deve ser usada como referencia sem esta correcao.

## 7. Historico recente
- R24: escada L compacta; ultima base visual funcional antes das tentativas de inversao.
- R25: placas solares e trilhos removidos; telhado preservado.
- R26: tentativa de inversao gerou regressao de geometria/testes/manifesto; posteriormente estabilizada.
- R27: reorganizou escada/corredor, mas utilizou semantica errada de frente/fundos. Necessita correcao de orientacao.

## 8. Incidentes que nao podem se repetir
- `manifest.json` desatualizado em relacao ao `model.json` causa `Download incompleto: model.json`.
- Faces do schema aceitam exatamente 4 vertices.
- `nome` do plugin: maximo 120 caracteres.
- `id`: maximo 48 caracteres.
- `tag`: maximo 40 caracteres.
- Nao considerar revisao pronta com GitHub Actions em `failure`.

## 9. Elementos estruturais de referencia
Pilares ativos: C01-C08 e C10. C09 e alias historico de C04.
Vigas de referencia: V01-V13.
Qualquer cabecalho ou reforco criado para abertura da escada e apenas geometria conceitual ate dimensionamento estrutural.

## 10. Regra para continuidade
Antes de toda revisao de escada, confirmar numericamente:
- DIREITA -> X alto.
- ESQUERDA -> X baixo.
- FUNDOS -> Y alto.
- FRENTE -> Y baixo.
