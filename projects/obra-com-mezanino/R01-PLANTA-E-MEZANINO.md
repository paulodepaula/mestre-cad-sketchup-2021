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
| Portao deslizante | nao modelado | nao modelado | - | Abre para direita; curso, motor e folgas desconhecidos |
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
1. Medir a distancia entre o muro frontal e a zona interna mais avancada do portao **totalmente aberto**, incluindo motor e elementos de manutencao. Isso determina o recuo tecnico seguro.
2. Confirmar a area util de implantacao no lado direito, considerando afastamentos municipais, instalacoes, passagem e altura do muro.
3. Definir em CAD o encaixe real da escada e patamar no mezanino; conferir o vazio para armarios e impressao 3D.
4. Medir ou definir com profissional o pe-direito terreo livre e mezanino livre antes de propor Z de cobertura/estruturas.

## Limite do gerador
Mestre CAD 1.4.1 suporta apenas `face` plana e `caixa` retangular. Nao modela nesta R01 perfis inclinados reais, escada parametrica, guarda-corpos, esquadrias ou analise de interferencias. A malha DAE e ilustrativa; somente estudo dimensional.
