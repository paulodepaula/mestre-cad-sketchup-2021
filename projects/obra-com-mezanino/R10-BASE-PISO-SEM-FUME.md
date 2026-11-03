# R10 - Grade metalica do piso e encontro com o vidro, SEM FUME

Modelo de estudo geometrico, NAO executivo. Nenhum codigo da extensao, atualizador, gerador CAD, workflow, release ou permissao foi alterado. Apenas projeto, documentacao e testes de geometria correspondentes.

## Base sob o piso
A R10 acrescenta 28 pecas separadas: 16 membros BM_L/BM_T da grade principal, oito BP_L/BP_T do patamar, dois apoios de esquadria BM_F01/BM_F02 sobre V05 e duas soleiras SG_ESQ/SG_DIR. Nao ha duas plataformas macicas de aco.

As travessas e longarinas ocupam o intervalo Z2690..2825mm. O painel de piso de 25mm permanece em Z2825..2850mm, agora com contatos geometricos nos apoios. O nivel do piso acabado continua 2,85m.

Os perfis da grade tem largura representativa de 50mm e altura disponivel de 135mm, com passo nominal de desenho de ate 400mm. Essas medidas sao HIPOTESES DE MODELAGEM: nao especificam perfil comercial, espessura do aco, capacidade ou vao admissivel. A chapa de 25mm tambem nao e produto escolhido. O mezanino tem uso previsto de escritorio/estacao de trabalho.

As barras junto a C03, C04, C05, C06 e C07 foram interrompidas ou ajustadas para nao atravessar o volume das colunas. A verificacao por coordenadas garante contato da grade com as vigas principais, direta ou indiretamente por outras barras. Isso NAO verifica resistencia das ligacoes.

## Encontro com vidro
Os dois paineis de vidro continuam com base Z2850 e plano Y5621. As soleiras SG_ESQ e SG_DIR, de representacao 50x25mm, ocupam Y5596..5646 e Z2825..2850. Elas fecham visualmente a folga horizontal de 25mm da R09 e encontram a base dos vidros, sem deixa-los flutuando. Os apoios inferiores BM_F01/BM_F02 nascem na V05 e chegam a face inferior das soleiras.

O vidro nao foi colocado sobre a placa cimenticia como apoio estrutural. Calcos, gaxetas, juntas, fixacoes, drenagem e perfil comercial da esquadria permanecem pendentes. A soleira sob o painel direito nao e piso transitavel e nao amplia o patamar sobre a reserva de escada.

## Preservacao
As coordenadas, tipos, tags e secoes dos 52 elementos da R09 foram preservadas, inclusive telhado, colunas, V05/V13, terreno, muro, vidro e piso. Nomes foram resumidos e os metadados vigentes consolidados; toda a R09 original, incluindo metadados historicos, esta preservada SEM modificacao em historico/model-R09.json.

Nao se aplicou cor fume, transparencia, material novo ou atualizacao de plugin. O vidro conserva a aparencia anterior e pode continuar opaco no importador atual. Agora ha 80 elementos, dentro do limite de 150 da extensao existente.

## Validacao
Testes de geometria verificam contatos, ausencia de interpenetracao das barras novas entre si e com as colunas, correspondencia dos 52 elementos anteriores, niveis do piso e soleiras, coplanaridade, envelope, DXF/DAE e integridade SHA-256 do manifesto. Tambem se preservaram testes negativos para unidades, IDs duplicados, coordenadas invalidas, adulteracao de arquivos e envelopes inconsistentes.

## Pendencias de engenharia
Calcular perfis, ligacoes, travamento, flechas, vibracao, cargas de escritorio e esquadrias, apoio das juntas do painel, recortes do piso nos pilares, escada, guarda-corpos e fundacoes. Os testes automaticos nao aprovam uso ou execucao da estrutura.
