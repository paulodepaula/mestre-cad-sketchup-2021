# frozen_string_literal: true
# Mestre CAD & SketchUp 2021
# Estudo GEOMETRICO de 4 x 6 m. NAO e projeto estrutural ou executivo.
# Execute dentro do SketchUp 2021 via Console Ruby:
# load 'C:/Projetos/gerar-volume-4x6.rb'

module MestreCad2021
  def self.gerar_volume_4x6
    major = Sketchup.version.to_i
    raise "Este exemplo foi preparado para SketchUp 2021 (21.x); detectado #{Sketchup.version}" unless major == 21

    largura_mm = 4000.0
    profundidade_mm = 6000.0
    pilar_mm = 100.0
    beiral_frontal_mm = 3000.0
    inclinacao = 0.07
    beiral_traseiro_mm = beiral_frontal_mm + profundidade_mm * inclinacao

    raise 'Medidas invalidas.' unless largura_mm > pilar_mm * 2 && profundidade_mm > pilar_mm * 2
    raise 'Altura de cobertura invalida.' unless beiral_frontal_mm > 0 && beiral_traseiro_mm > 0

    model = Sketchup.active_model
    model.start_operation('Estudo 4x6 m - Mestre CAD', true)

    begin
      raiz = model.entities.add_group
      raiz.name = 'ESTUDO_4X6_NAO_ESTRUTURAL'
      raiz.layer = model.layers.add('CAD_ESTUDO_4X6')

      # Planta: superficie de referencia, sem espessura construtiva.
      piso = raiz.entities.add_group
      piso.name = 'PISO_REFERENCIA_4000x6000'
      piso.entities.add_face(
        [0.mm, 0.mm, 0.mm],
        [largura_mm.mm, 0.mm, 0.mm],
        [largura_mm.mm, profundidade_mm.mm, 0.mm],
        [0.mm, profundidade_mm.mm, 0.mm]
      ) || raise('Falha ao criar a planta de referencia.')

      # Pilar ilustrativo retangular, com secao nao dimensionada.
      posicoes = [
        [0.0, 0.0, beiral_frontal_mm, 'FRONTAL_ESQ'],
        [largura_mm - pilar_mm, 0.0, beiral_frontal_mm, 'FRONTAL_DIR'],
        [0.0, profundidade_mm - pilar_mm, beiral_traseiro_mm, 'TRASEIRO_ESQ'],
        [largura_mm - pilar_mm, profundidade_mm - pilar_mm, beiral_traseiro_mm, 'TRASEIRO_DIR']
      ]

      posicoes.each do |x, y, altura, nome|
        grupo = raiz.entities.add_group
        grupo.name = "PILAR_ESTUDO_#{nome}_100x100"
        face = grupo.entities.add_face(
          [x.mm, y.mm, 0.mm],
          [(x + pilar_mm).mm, y.mm, 0.mm],
          [(x + pilar_mm).mm, (y + pilar_mm).mm, 0.mm],
          [x.mm, (y + pilar_mm).mm, 0.mm]
        )
        raise "Falha ao criar a face do pilar #{nome}." unless face

        # Faces no solo (Z=0) nascem voltadas para baixo no SketchUp.
        # Reorientar evita criar pilares abaixo do piso.
        face.reverse! if face.normal.z < 0
        raise "Base do pilar #{nome} invertida." unless face.normal.z > 0
        face.pushpull(altura.mm)
      end

      # Somente plano de referencia da cobertura, sem espessura e sem ligacoes.
      cobertura = raiz.entities.add_group
      cobertura.name = 'COBERTURA_REFERENCIA_UMA_AGUA_7PCT'
      face_cobertura = cobertura.entities.add_face(
        [0.mm, 0.mm, beiral_frontal_mm.mm],
        [largura_mm.mm, 0.mm, beiral_frontal_mm.mm],
        [largura_mm.mm, profundidade_mm.mm, beiral_traseiro_mm.mm],
        [0.mm, profundidade_mm.mm, beiral_traseiro_mm.mm]
      )
      raise 'Falha ao criar plano de cobertura.' unless face_cobertura

      # BoundingBox: width = X, height = Y, depth = Z na API SketchUp.
      bbox = raiz.bounds
      raise 'Geometria sem bounding box valido.' unless bbox.valid?

      obtido_mm = [bbox.width.to_f.to_mm, bbox.height.to_f.to_mm, bbox.depth.to_f.to_mm]
      esperado_mm = [largura_mm, profundidade_mm, beiral_traseiro_mm]
      nomes = %w[X Y Z]
      nomes.each_with_index do |eixo, i|
        erro_mm = (obtido_mm[i] - esperado_mm[i]).abs
        raise "Dimensao #{eixo} fora do esperado (erro #{erro_mm.round(3)} mm)." if erro_mm > 0.5
      end

      model.commit_operation
      puts 'PASS: estudo geometrico criado em grupo nomeado.'
      puts "Dimensoes conferidas X/Y/Z: #{obtido_mm.map { |v| v.round(1) }.join(' / ')} mm"
      puts 'ATENCAO: pilares, ligacoes e cobertura sao ilustrativos; sem calculo estrutural.'
      raiz
    rescue StandardError => e
      model.abort_operation
      warn "ERRO - Operacao revertida: #{e.class}: #{e.message}"
      raise
    end
  end
end

MestreCad2021.gerar_volume_4x6
