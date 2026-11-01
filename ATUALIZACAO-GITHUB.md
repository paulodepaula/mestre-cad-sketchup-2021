# Distribuicao Mestre CAD por GitHub

Repositorio publico: `paulodepaula/mestre-cad-sketchup-2021`.
A extensao instalada no SketchUp verifica a API oficial de Releases ao clicar em **Verificar atualizacoes no GitHub**.

## Processo

1. Desenvolvedor altera codigo Ruby e versionamento em ambos os arquivos do loader e atualizador.
2. Push para `main` aciona testes offline no GitHub Actions.
3. Workflow empacota `bridge/mestre_cad_2021.rb` e toda a pasta `bridge/mestre_cad_2021/` em RBZ, verifica conteudo do ZIP e publica Release estavel.
4. No SketchUp 2021, o usuario verifica atualizacoes, confirma, faz download do RBZ via HTTPS, compara SHA-256 da API do GitHub, salva backup e instala.
5. Reinicie o SketchUp para ativar a nova versao.

## Limites e seguranca

- Requer repositorio publico para consulta sem token.
- Nao consulta codigo do branch `main` para executar diretamente. Apenas releases com nome esperado e SHA-256 declarado.
- A confirmacao do usuario e obrigatoria. O programa nao executa em segundo plano nem recebe comandos remotos.
- Nao e uma sincronizacao automatica de projetos `.skp`.
- O SHA-256 confere integridade dos bytes mas nao protege contra comprometimento do proprio repositorio.
- O projeto 4 x 6 m e ilustrativo; precisa de engenheiro/projetista habilitado para dimensionamento.
