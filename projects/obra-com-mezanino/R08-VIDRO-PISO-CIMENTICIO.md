# R08 - Extensao da V05, montante C07 ate V13 e paineis superiores de vidro

**Revisao de estudo nao executivo, com fonte no model.json para sincronizacao pelo plugin do SketchUp.**

## Alteracoes de geometria
- **V05**: origem (6461,5521,2510)mm, dimensoes de estudo **4000x100x180mm** (antes 3000x100x180). A viga chega ate a borda externa da C10 (X10461) e sobrepoe a largura desta coluna em projecao. Esta ligacao e meramente geometrica, **sem capacidade portante verificada**.
- **C07**: origem (9361,5521,0)mm, agora 100x100x**5355mm** (antes 2510mm de altura), encontro geometrico com a **face inferior inclinada da V13** no bordo de X9361. A diferenca de +5 mm no nivel de X9461 deve ser tratada em detalhe de ligacao/chapas de topo no futuro. **C07 continua nascendo no piso**; sua funcao como montante de vidro nao transforma V13 em apoio capaz de sustentar o mezanino sem dimensionamento.
- **VF08_SUP_ESQ** e **VF08_SUP_DIR**: dois panos superiores em `VIDRO_FUNDOS_ESTUDO`, alinhados ao conjunto C04/C07/C10 e V05, no plano Y5621mm, iniciando em Z2850mm (topo do mezanino) e terminando na geratriz inferior inclinada da V13 (5%). A divisao acontece em C07. Estes panos sao **faces de referencia**, sem vidro, esquadria, transparencia e perfis comerciais dimensionados.
- A face envidracada esta na **linha recuada do mezanino**, cerca de 1m da borda da oficina voltada para C-D. **Fechamento do trecho inferior, porta de acesso e portas de emergencia permanecem em aberto** para evitar bloquear a entrada sem definicao expressa.
- Telhado COB_R03, restantes pilares, vigas, terreno T01 e muro B-C **intactos**.

## Decisao de piso: placa cimenticia em avaliacao
- O mezanino permanece com volume geometrico **160mm** (dos Z2690 a Z2850), **reserva de espessura para uma futura composicao**, nao uma placa cimenticia macica de 160mm.
- **Placa comum de revestimento de parede nao deve ser presumida como piso portante**. Precisa de produto explicitamente homologado pelo fabricante para piso/mezanino, com ficha tecnica, carga de uso, reacoes e detalhamento de travessas secundarias.
- Referencia A: **Superboard Piso 14mm** (sistema residencial de carga anunciada ate 250kg/m2, com apoios a cada 400mm, sujeitos ao sistema/ficha e dimensionamento, nao adotados como carga de projeto).
- Referencia B: **placa cimenticia NTF Infibra para mezaninos**: 20mm com referencia de apoio a 400mm; 25/30mm com apoios de 400 a 600mm (consultar tabela de carga da linha adquirida).
- Referencia C: painel de mezanino **LP Mezanino / painel wall** ou outro sistema composto para vencer vao maior e reduzir estrutura secundaria, sujeito a tabela de uso/apoios.
- O vao do piso e a distribuicao de carga necessitam de **vigas secundarias/travessas**. V05/V03/V04 e uma chapa fina isolada **nao definem um piso pronto ou estruturalmente dimensionado**.
- **Nao foi escolhida espessura de placa nem alterado o nivel do mezanino**. A ideia de placa cimenticia sera avaliada conforme uso do mezanino (escritorio, armazenagem leve, ferramentas e cargas concentradas) e capacidade da estrutura.

## Fontes tecnicas de fabricante consultadas (02/11/2026)
- Gypsum/Etex - placa Superboard Piso 14mm e a necessidade de apoio 400mm (aplicacao e cargas referenciadas pelo fabricante): https://www.gypsum.com.br/pt-br/centro-de-apoio/blog/142210/placa-cimenticia-no-piso/
- Infibra - NTF para mezaninos e espacamentos nominais de apoio: https://www.infibra.com.br/post/como-substituir-o-painel-wall-pela-placa-ciment%C3%ADcia-ntf-em-projetos-de-mezanino
- Brasilit - produtos de fechamentos e manual de placa cimenticia com especificacao de perfis metalicos: https://www.brasilit.com.br/placa-cimenticia
- LP Brasil - catalogo do painel LP Mezanino: https://www.lpbrasil.com.br/wp-content/uploads/2019/10/20200826-Catalogo-MEzanino.pdf

## Pendencias
**Engenheiro estrutural com ART** deve definir carregamento de mezanino, servico das vigas e das colunas de 3mm, detalhamento de V05-C10 e C07-V13, perfis e parafusos/soldas, projeto de estabilidade e fundacoes. **Engenheiro/projetista de esquadrias** deve verificar vidro de seguranca adequado ao uso e normas, carga de vento e fixacoes, juntas, porta e seguranca das bordas do mezanino. 
