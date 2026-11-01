# Mestre CAD & SketchUp 2021

Extensao Ruby de modelagem geometrica por medidas para SketchUp 2021 (21.x).

- Importa arquivos JSON com medidas em milimetros e gera grupos editaveis.
- Confere dimensoes geometricas e oferece auditoria do grupo criado.
- Inclui exemplo conceitual de oficina 4 x 6 m; **nao e projeto estrutural**.
- Depois da instalacao inicial, permite verificar e instalar atualizacoes publicadas como GitHub Releases, com verificacao SHA-256, confirmacao e backup.

## Primeira instalacao

1. Abra a pagina **Releases** deste repositorio e baixe o `mestre-cad-bridge-2021-v1.2.1.rbz`.
2. No SketchUp 2021: **Extensoes > Gerenciador de Extensoes > Instalar Extensao**.
3. Instale o RBZ, reinicie o SketchUp e abra um modelo vazio.
4. Menu **Extensoes > Mestre CAD 2021 > Gerar exemplo 4 x 6 m**.
5. Confirme que o envelope esperado e **4.000 x 6.000 x 3.420 mm** e salve o SKP de teste.

## Atualizar sem baixar manualmente

No menu Mestre CAD, clique **Verificar atualizacoes no GitHub**.
A extensao consulta somente releases publicas do repositorio configurado; novas versoes exigem confirmacao antes de instalar e o processo guarda backup local.
O projeto aberto nao e alterado pelo atualizador.

## Lancamentos

No push para `main` alterando `bridge/`, `examples/` ou o workflow, GitHub Actions roda testes Ruby offline, cria RBZ e publica release estavel `vX.Y.Z` caso a tag ainda nao exista.
Para novas versoes, ajuste **ambos** `bridge/mestre_cad_2021.rb` (`ext.version`) e `bridge/mestre_cad_2021/updater.rb` (`VERSION`) antes do push.

O exemplo `bridge/mestre_cad_2021/exemplo-4x6.json` faz parte do RBZ; uma verificacao de empacotamento impede release sem o arquivo.

**Testes offline nao substituem homologacao no SketchUp 2021.**
