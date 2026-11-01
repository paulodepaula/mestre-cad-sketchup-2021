# Mestre CAD & SketchUp 2021

Repositório do plugin e, em `projects/`, dos arquivos de projeto gerados automaticamente no GitHub.

## Projeto: obra com mezanino

O arquivo fonte de medidas está em [`projects/obra-com-mezanino/model.json`](projects/obra-com-mezanino/model.json). Cada alteração do JSON dispara o workflow **Gerar arquivos CAD a partir do projeto**, que valida os dados e publica:

- [Planta DXF](projects/obra-com-mezanino/cadcraft/planta.dxf) e [elevações DXF](projects/obra-com-mezanino/cadcraft/elevacoes.dxf) para o CadCraft ou outro CAD compatível.
- [Modelo DAE](projects/obra-com-mezanino/sketchup/modelo.dae) 3D para importar no SketchUp 2021.
- [Manifesto de integridade](projects/obra-com-mezanino/manifest.json) com SHA-256.

**Ainda não existe `.skp` diretamente gerado no GitHub:** para isso precisamos integrar o SDK oficial e habilitar um ambiente compatível. Veja [documentação](docs/SKP-NATIVO.md). Também não há geração nativa de `.dwg` nesta fase. O projeto R00 usa medidas ilustrativas e não dimensiona um mezanino.

## SketchUp 2021

Na seção [Releases](https://github.com/paulodepaula/mestre-cad-sketchup-2021/releases), instale a versão 1.3.0 ou posterior do `.rbz` uma vez. No SketchUp, use:

1. **Extensões > Mestre CAD 2021 > Sincronizar arquivos CAD do GitHub...** (baixa JSON/DXF/DAE e verifica SHA-256 sem sobrescrever alterações locais).
2. **Extensões > Mestre CAD 2021 > Importar projeto sincronizado...** (cria grupos editáveis a partir do JSON; salve como `.skp`).
3. **Extensões > Mestre CAD 2021 > Verificar atualizações no GitHub...** para atualizar a própria extensão quando necessário.

O diretório local padrão é `Documentos/MestreCAD/projetos/obra-com-mezanino`. Os arquivos `.skp` locais não são alterados pelo comando de sincronização. Você também pode usar `git clone` e `git pull --ff-only` para obter os arquivos, sem a extensão.

## Desenvolvimento

Código Ruby está em `bridge/`; executa no SketchUp 21.x (Ruby 2.7). Os testes da extensão rodam offline no GitHub Actions, mas a execução gráfica depende de homologação no SketchUp 2021.

O gerador Python não usa dependências de terceiros:

```bash
python3 tools/build_project.py projects/obra-com-mezanino/model.json
python3 tools/build_project.py projects/obra-com-mezanino/model.json --check
python3 -m unittest discover -s tools/tests -v
```
