# Obra com mezanino - R13

Fonte unica: model.json no GitHub. SketchUp 2021 e CadCraft recebem os arquivos sincronizados. Modelo de estudo, NAO executivo.

## Alteracao R13
- Somente **C02** foi reduzida de 150x150mm para **100x100mm**, mantendo parede nominal **3mm** e altura **5420mm**.
- Origem passa de X10311 para X10361, preservando a face externa X10461 junto a B-C; Y inicial 3571 mantido.
- Eliminada a invasao de 50mm da C02 na reserva da escada. A reserva permanece **900x3200mm**, limitada a face C07/C10 em Y5621, com chegada no patamar a Z2715.
- C02 encontra a viga **V01 da cobertura** e a **V10 do mezanino**. NAO foi classificada como sem carga; a reducao precisa de verificacao estrutural.
- Os outros **100 elementos** permanecem identicos a R12. C03-C06 continuam 150x150x3mm, grade secundaria 50x50 entre vigas, piso 25mm de estudo em Z2690..2715 e vidros sem fume.
- Oficina **4000x6000mm** mais passarela de 1000mm; telhado, lote e muro inalterados. Total **101 elementos**.

Detalhamento: [R13-C02-100X100.md](R13-C02-100X100.md).
Historico integral: [historico/model-R12.json](historico/model-R12.json).
Metodo de trabalho: [AGENTS.md](AGENTS.md).

## Limites
Nao executar a estrutura a partir das secoes ilustrativas. Calcular cargas, flambagem, estabilidade, vigas, soldas, bases, fundacoes e escada. A ausencia de interferencia geometrica nao constitui aprovacao de seguranca ou de uso.
