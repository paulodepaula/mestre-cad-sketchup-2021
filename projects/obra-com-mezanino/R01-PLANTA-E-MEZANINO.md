# R01 - Levantamento dimensional, planta e proposta de mezanino

## Referenciais e proveniencia
- Modelo original: R00 arquivado em `historico/model-R00.json`.
- Convencao: X direita olhando a frente; Y fundo; Z altura; todas as cotas em milimetros; X=0 e face externa esquerda da oficina, Y=0 face frontal proposta.
- Fonte das cotas confirmadas: definicoes do proprietario na sessao de anteprojeto. Fotografias apenas como referencias de aparencia, sem uso para extrair medidas.
- **Nenhuma sapata, pilar, viga, perfil, inclinação ou cobertura foi dimensionada nesta revisao.**

## Quadro dimensional

| Elemento | Faixa X (mm) | Faixa Y (mm) | Z (mm) | Estado |
|---|---:|---:|---:|---|
| Area principal - terreo | 0..4000 | 0..6000 | 0 | Largura/profundidade definidas; piso e face de estudo |
| Passarela lateral direita | 4000..5000 | 0..6000 | 0 | Largura definida; extensao de 6000 e proposta |
| Mezanino - localizacao R01 | 1000..4000 | 2000..6000 | 2850 | Area 12m2, posicao e nivel ainda hipoteticos |
| Reserva da escada (nao e escada desenhada) | 0..900 | 0..4200 | 0 | Hipotese, sujeita a calculo de degraus, patamar e acesso |
| Terreno frontal | nao modelado | nao modelado | - | Frente de 10000 informada; posicao da oficina no lote por medir |
| Portao deslizante | nao modelado | nao modelado | - | Abre para direita; extremidade mais interna a 300 mm da face interna do muro frontal (medida informada); curso horizontal e folga tecnica ainda pendentes |
| Cobertura/pilares/fundacoes | nao modelados | nao modelados | - | Pendentes de arquitetura, engenharia e sondagem |

## Checagens geometricas que podem ser reproduzidas
- Oficina 4000 x 6000 = 24,00 m2; diagonal = 7211,10 mm.
- Passarela 1000 x 6000 = 6,00 m2 como **hipotese de extensao**.
- Conjunto 5000 x 6000 = 30,00 m2 de envelope horizontal (nao e area construída legal).
- Mezanino proposto 3000 x 4000 = 12,00 m2.
- Reservar 900 x 4200 mm para escada **nao prova** atendimento de circulacao, geometria dos degraus ou altura livre.
- A face em Z2850 define apenas a cota de estudo do piso superior, NAO altura livre, espessura de laje nem altura do telhado.
- Existe separacao nominal de 100 mm entre borda da reserva da escada (X900) e inicio do mezanino (X1000); sera necessario um patamar e ajuste de geometria, ainda NAO modelados. Nao construir como esta.

## Decisoes para avancar R02
1. **Medida recebida:** portao totalmente aberto avanca 300 mm para dentro do lote a partir da face interna do muro frontal, incluindo motor. Esta medida define somente a faixa de interferencia, **nao o recuo de implantacao aprovado**. Ainda definir folga de manutencao e adequacao ao codigo municipal.
2. Medir a largura livre de implantacao no lado direito e o alinhamento transversal do portao, considerando afastamentos municipais, instalacoes e passagem. Ate essa confirmacao, nao deslocar coordenadas do projeto para o terreno.
3. Definir em CAD o encaixe real da escada e patamar no mezanino; conferir o vazio para armarios e impressao 3D.
4. Medir ou definir com profissional o pe-direito terreo livre e mezanino livre antes de propor Z de cobertura/estruturas.

## Limite do gerador
Mestre CAD 1.4.1 suporta apenas `face` plana e `caixa` retangular. Nao modela nesta R01 perfis inclinados reais, escada parametrica, guarda-corpos, esquadrias ou analise de interferencias. A malha DAE e ilustrativa; somente estudo dimensional.

## Atualizacao de levantamento - portao frontal

- **300 mm**: distancia informada entre a face interna do muro frontal e a extremidade mais interna ocupada pelo portao deslizante ao abrir para a direita, incluindo o motor.
- **Nao equivale a recuo aprovado:** a face externa da nova edificacao deve ficar fora da interferencia do portao, com folga tecnica e manutencao; sua distancia definitiva do muro fica em aberto.
- Sem levantamento do alinhamento X, a ocupacao do portao nao pode ser transformada em faixa de 5.000 mm de largura no CAD. Portanto, **modelo geometrico R01 permanece inalterado** (coordenadas X/Y/Z locais da edificacao).
- Capturas do SketchUp e CadCraft mostram os quatro planos de estudo esperados: nao ha pilares, fechamento, escada executiva ou cobertura nesta revisao. A figura em perspectiva pode parecer volume por causa das linhas de referencia, mas o mezanino e uma face sem espessura.
