# frozen_string_literal: true
# Mestre CAD Bridge 1.4.1 - SketchUp Desktop 2021 / Ruby 2.7.
# Sem rede, sem execucao arbitraria de JSON, sem alterar/apagar entidades existentes.
require 'sketchup.rb'
require 'json'
require_relative 'updater'
require_relative 'project_sync'

module MestreCAD
  module SketchUp2021
    extend self

    SCHEMA = 'mestre-cad-geometria-v1'.freeze
    DICT = 'MestreCAD2021'.freeze
    TOL_MM = 0.5
    MAX_ELEMENTS = 150
    MAX_ENVELOPE_MM = 500_000.0

    def check_version!
      versao = Sketchup.version.to_s
      raise "Requer SketchUp 2021 (21.x). Detectado: #{versao}" unless versao.to_i == 21
    end

    def number!(value, context, allow_zero = true)
      raise ArgumentError, "#{context}: use numero (mm)." unless value.is_a?(Numeric) && value.finite?
      min = allow_zero ? 0.0 : 0.0
      raise ArgumentError, "#{context}: valor negativo ou zero nao permitido." if allow_zero ? value < min : value <= min
      raise ArgumentError, "#{context}: medida excessiva." if value > MAX_ENVELOPE_MM
      value.to_f
    end

    def vec3!(value, context, allow_zero = true)
      raise ArgumentError, "#{context}: exige vetor com 3 numeros." unless value.is_a?(Array) && value.size == 3
      value.each_with_index.map { |v, i| number!(v, "#{context}[#{i}]", allow_zero) }
    end

    def field_string!(object, key, context, max_size = 120)
      value = object[key]
      raise ArgumentError, "#{context}.#{key}: texto invalido." unless value.is_a?(String) && !value.strip.empty? && value.length <= max_size
      value.strip
    end

    def bbox_for(element)
      if element['tipo'] == 'caixa'
        o = element['origem_mm']
        d = element['dimensoes_mm']
        [o.map(&:to_f), o.each_with_index.map { |v, i| v.to_f + d[i].to_f }]
      else
        coords = element['pontos_mm']
        [3.times.map { |i| coords.map { |v| v[i] }.min.to_f },
         3.times.map { |i| coords.map { |v| v[i] }.max.to_f }]
      end
    end

    def plane_valid!(points, id)
      # Testa se os quatro vertices formam uma superficie coplanar nao degenerada.
      a, b, c, d = points
      u = 3.times.map { |i| b[i] - a[i] }
      v = 3.times.map { |i| c[i] - a[i] }
      cross = [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0]]
      norm = Math.sqrt(cross.inject(0.0) { |s, val| s + val*val })
      raise ArgumentError, "#{id}: face degenerada." if norm < 0.5
      w = 3.times.map { |i| d[i] - a[i] }
      dist = cross.each_with_index.inject(0.0) { |s, (n, i)| s + n*w[i] }.abs / norm
      raise ArgumentError, "#{id}: face nao coplanar (#{dist.round(2)} mm)." if dist > TOL_MM
      # O SketchUp rejeita alguns contornos cruzados; nao inventar superficies.
    end

    def validate!(data)
      raise ArgumentError, 'Raiz JSON deve ser objeto.' unless data.is_a?(Hash)
      raise ArgumentError, 'Schema nao suportado.' unless data['schema'] == SCHEMA
      raise ArgumentError, 'A unidade obrigatoria e mm.' unless data['unidades'] == 'mm'
      field_string!(data, 'nome', 'projeto')
      field_string!(data, 'revisao', 'projeto', 20)
      envelope = data['envelope_mm']
      raise ArgumentError, 'envelope_mm deve ser objeto.' unless envelope.is_a?(Hash)
      xyz = %w[x y z].map { |k| number!(envelope[k], "envelope_mm.#{k}", false) }
      elementos = data['elementos']
      raise ArgumentError, "elementos: deve conter de 1 a #{MAX_ELEMENTS} itens." unless elementos.is_a?(Array) && elementos.length.between?(1, MAX_ELEMENTS)
      ids = {}
      all_mins = [Float::INFINITY]*3
      all_maxs = [-Float::INFINITY]*3
      elementos.each_with_index do |e, n|
        raise ArgumentError, "elemento #{n}: deve ser objeto." unless e.is_a?(Hash)
        id = field_string!(e, 'id', "elemento #{n}", 48)
        raise ArgumentError, "ID repetido: #{id}" if ids.key?(id)
        ids[id] = true
        field_string!(e, 'nome', id)
        tag = field_string!(e, 'tag', id, 40)
        raise ArgumentError, "#{id}: tag so pode ter letras maiusculas, numeros e _." unless tag.match?(/\A[A-Z][A-Z0-9_]*\z/)
        case e['tipo']
        when 'caixa'
          vec3!(e['origem_mm'], "#{id}.origem_mm")
          vec3!(e['dimensoes_mm'], "#{id}.dimensoes_mm", false)
        when 'face'
          pts = e['pontos_mm']
          raise ArgumentError, "#{id}: face precisa de 4 pontos." unless pts.is_a?(Array) && pts.length == 4
          pts.each_with_index { |p, i| vec3!(p, "#{id}.ponto#{i}") }
          plane_valid!(pts, id)
        else
          raise ArgumentError, "#{id}: tipo nao suportado (use caixa ou face)."
        end
        min_e, max_e = bbox_for(e)
        3.times do |i|
          raise ArgumentError, "#{id}: fora do envelope no eixo #{%w[X Y Z][i]}." if max_e[i] > xyz[i] + TOL_MM
          all_mins[i] = [all_mins[i], min_e[i]].min
          all_maxs[i] = [all_maxs[i], max_e[i]].max
        end
      end
      3.times do |i|
        raise ArgumentError, "O conjunto nao comeca em zero no eixo #{%w[X Y Z][i]}." if all_mins[i].abs > TOL_MM
        raise ArgumentError, "Envelope nao confere no eixo #{%w[X Y Z][i]}. Conteudo ate #{all_maxs[i]} mm, contrato #{xyz[i]} mm." if (all_maxs[i] - xyz[i]).abs > TOL_MM
      end
      "PASS: #{elementos.length} elementos; envelope X/Y/Z #{xyz.map { |v| v.round(1) }.join(' / ')} mm."
    end

    def read_json(path)
      raise ArgumentError, 'Arquivo .json necessario.' unless path.to_s.downcase.end_with?('.json')
      raise ArgumentError, 'Arquivo muito grande (limite: 1 MB).' if File.size(path) > 1_000_000
      data = JSON.parse(File.read(path, encoding: 'UTF-8'))
      validate!(data)
      data
    end

    def p3(coords)
      coords.map { |mm| mm.to_f.mm }
    end

    def add_element(entities, e, layers)
      element_group = entities.add_group
      element_group.name = "#{e['id']} - #{e['nome']}"
      layer_name = "MC21_#{e['tag']}"
      tag = layers[layer_name] || layers.add(layer_name)
      element_group.layer = tag
      element_group.set_attribute(DICT, 'id', e['id'])
      element_group.set_attribute(DICT, 'expected', JSON.generate(e))
      if e['tipo'] == 'caixa'
        x, y, z = e['origem_mm']
        dx, dy, dz = e['dimensoes_mm']
        contour = [[x,y,z], [x+dx,y,z], [x+dx,y+dy,z], [x,y+dy,z]].map { |p| p3(p) }
        face = element_group.entities.add_face(contour)
        raise "#{e['id']}: nao foi possivel criar base." unless face
        # SketchUp always orients a face at Z=0 downwards, even if its
        # vertex winding is counter-clockwise. PushPull follows the normal.
        # Correct the orientation before extruding every prism in +Z.
        face.reverse! if face.normal.z < 0
        raise "#{e['id']}: base nao esta horizontal." unless face.normal.z > 0
        face.pushpull(dz.mm)
      else
        face = element_group.entities.add_face(e['pontos_mm'].map { |p| p3(p) })
        raise "#{e['id']}: nao foi possivel criar plano." unless face
      end
      element_group
    end

    def mm_bbox(group)
      box = group.bounds
      raise "Geometria vazia: #{group.name}." unless box.valid?
      [box.min, box.max].map { |point| [point.x.to_mm, point.y.to_mm, point.z.to_mm] }
    end

    def difference(expected, actual, label, issues)
      2.times do |ext|
        3.times do |axis|
          err = (expected[ext][axis] - actual[ext][axis]).abs
          issues << "#{label}: #{ext == 0 ? 'min' : 'max'} #{%w[X Y Z][axis]} difere #{err.round(2)} mm" if err > TOL_MM
        end
      end
    end

    def verify_group(root)
      raw = root.get_attribute(DICT, 'data')
      raise ArgumentError, 'Grupo nao foi gerado pelo Mestre CAD.' unless raw.is_a?(String)
      data = JSON.parse(raw)
      validate!(data)
      issues = []
      expected_root = [[0.0, 0.0, 0.0], %w[x y z].map { |k| data['envelope_mm'][k].to_f }]
      actual_root = mm_bbox(root)
      # O conjunto pode ser movido sem mudar dimensoes: referencial normalizado.
      root_min = actual_root[0]
      root_size = actual_root[1].each_with_index.map { |v, i| v-root_min[i] }
      3.times do |axis|
        err = (root_size[axis]-expected_root[1][axis]).abs
        issues << "Conjunto: eixo #{%w[X Y Z][axis]} difere #{err.round(2)} mm" if err > TOL_MM
      end
      children = root.entities.grep(Sketchup::Group)
      expected_ids = data['elementos'].map { |e| e['id'] }
      seen = {}
      children.each do |group|
        id = group.get_attribute(DICT, 'id')
        issues << "Grupo estranho: #{group.name}" unless expected_ids.include?(id)
        issues << "Grupo duplicado: #{id}" if seen[id]
        seen[id] = group if expected_ids.include?(id)
      end
      data['elementos'].each do |e|
        group = seen[e['id']]
        unless group
          issues << "Elemento ausente: #{e['id']}"
          next
        end
        difference(bbox_for(e), mm_bbox(group), e['id'], issues)
        if e['tipo'] == 'face'
          issues << "#{e['id']}: face ausente" if group.entities.grep(Sketchup::Face).empty?
        else
          issues << "#{e['id']}: prisma incompleto" if group.entities.grep(Sketchup::Face).length < 6
        end
      end
      [issues.empty?, issues, "X/Y/Z: #{root_size.map { |v| v.round(1) }.join(' / ')} mm; #{children.length} grupos"]
    end

    def build(data, auto_save: false)
      check_version!
      resumo = validate!(data)
      msg = "#{data['nome']} / #{data['revisao']}\n#{resumo}\n\nAdicionar novo grupo ao modelo aberto?\nElementos existentes NAO serao apagados.\nA estrutura e um ESTUDO, nao um calculo estrutural."
      return nil unless UI.messagebox(msg, MB_YESNO) == IDYES
      model = Sketchup.active_model
      raise 'Nao ha modelo aberto.' unless model
      model.start_operation('Mestre CAD: importar geometria', true)
      begin
        root = model.entities.add_group
        root.name = "MESTRE_CAD_#{data['revisao']} - #{data['nome']}"
        root.layer = model.layers['MC21_CONJUNTOS'] || model.layers.add('MC21_CONJUNTOS')
        root.set_attribute(DICT, 'schema', SCHEMA)
        root.set_attribute(DICT, 'data', JSON.generate(data))
        data['elementos'].each { |e| add_element(root.entities, e, model.layers) }
        ok, issues, details = verify_group(root)
        raise "Falha na auditoria: #{issues.first(8).join('; ')}" unless ok
        model.commit_operation
        model.selection.clear
        model.selection.add(root)
        puts "MESTRE CAD PASS: #{resumo} - #{details}"
        unless auto_save
          UI.messagebox("Projeto criado e verificado.\n#{details}\n\nSalve uma COPIA .skp no SketchUp.\nNao e projeto executivo.")
        end
        root
      rescue StandardError => e
        model.abort_operation
        raise e
      end
    end

    def import_file
      check_version!
      path = UI.openpanel('Mestre CAD - escolher projeto JSON', '', 'Projetos JSON|*.json||')
      return unless path
      build(read_json(path))
    rescue StandardError => e
      warn "MESTRE CAD FALHA: #{e.class}: #{e.message}"
      UI.messagebox("Falha ao importar: #{e.message}")
    end

    def validate_file
      check_version!
      path = UI.openpanel('Mestre CAD - validar JSON (sem modelar)', '', 'Projetos JSON|*.json||')
      return unless path
      msg = validate!(read_json(path))
      puts "MESTRE CAD #{msg}"
      UI.messagebox(msg)
    rescue StandardError => e
      warn "MESTRE CAD FALHA: #{e.class}: #{e.message}"
      UI.messagebox("JSON invalido: #{e.message}")
    end

    def example
      check_version!
      path = File.join(__dir__, 'exemplo-4x6.json')
      build(read_json(path))
    rescue StandardError => e
      warn "MESTRE CAD FALHA: #{e.class}: #{e.message}"
      UI.messagebox("Falha no exemplo: #{e.message}")
    end

    def audit_selection
      check_version!
      model = Sketchup.active_model
      groups = model.selection.grep(Sketchup::Group)
      raise ArgumentError, 'Selecione exatamente um grupo gerado pelo Mestre CAD.' unless groups.length == 1 && model.selection.length == 1
      ok, issues, info = verify_group(groups.first)
      puts "MESTRE CAD #{ok ? 'PASS' : 'FAIL'} - #{info}"
      issues.each { |s| puts "  FALHA: #{s}" }
      UI.messagebox("#{ok ? 'PASS' : 'FAIL'} - #{info}\n#{issues.first(8).join("\n")}")
    rescue StandardError => e
      warn "MESTRE CAD FALHA: #{e.class}: #{e.message}"
      UI.messagebox("Nao foi possivel conferir: #{e.message}")
    end

    unless file_loaded?(__FILE__)
      menu = UI.menu('Extensions').add_submenu('Mestre CAD 2021')
      menu.add_item('Validar projeto JSON (sem alterar modelo)...') { validate_file }
      menu.add_item('Importar projeto JSON como grupos...') { import_file }
      menu.add_item('Gerar exemplo 4 x 6 m...') { example }
      menu.add_item('Conferir grupo selecionado...') { audit_selection }
      menu.add_separator
      menu.add_item('Sincronizar arquivos CAD do GitHub...') { ProjectSync.sync_dialog }
      menu.add_item('Importar projeto sincronizado...') { ProjectSync.import_synced }
      menu.add_item('Salvar copia SKP do projeto sincronizado...') { ProjectSync.save_selected_skp }
      menu.add_separator
      menu.add_item('Configurar repositorio GitHub...') { Updater.configure_repository }
      menu.add_item('Verificar atualizacoes no GitHub...') { Updater.check_for_updates }
      menu.add_item('Restaurar versao anterior...') { Updater.restore_previous }
      file_loaded(__FILE__)
    end
  end
end
