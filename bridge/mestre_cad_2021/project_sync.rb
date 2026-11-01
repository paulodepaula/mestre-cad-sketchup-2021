# frozen_string_literal: true
# Mestre CAD 2021 - sincronia READ-ONLY de artefatos de projeto do GitHub.
# Nunca sobrescreve .skp nem modifica modelos abertos durante o download.
require 'json'
require 'net/http'
require 'uri'
require 'digest'
require 'fileutils'
require 'tmpdir'
require 'securerandom'
require 'time'

module MestreCAD
  module SketchUp2021
    module ProjectSync
      extend self

      REPO = 'paulodepaula/mestre-cad-sketchup-2021'.freeze
      BRANCH = 'main'.freeze
      PROJECT = 'obra-com-mezanino'.freeze
      REMOTE = "projects/#{PROJECT}".freeze
      FILES = %w[model.json cadcraft/planta.dxf cadcraft/elevacoes.dxf sketchup/modelo.dae].freeze
      MANIFEST = 'manifest.json'.freeze
      STATE = '.mestre-cad-sync.json'.freeze
      SCHEMA = 'mestre-cad-sync-v1'.freeze
      MAX_FILE_BYTES = 8 * 1024 * 1024
      MAX_MANIFEST_BYTES = 32 * 1024

      def local_root
        File.join(Dir.home, 'Documents', 'MestreCAD', 'projetos', PROJECT)
      end

      def sha256(payload)
        Digest::SHA256.hexdigest(payload)
      end

      def remote_url(relative)
        raise ArgumentError, 'Caminho remoto nao permitido.' unless (FILES + [MANIFEST]).include?(relative)
        "https://raw.githubusercontent.com/#{REPO}/#{BRANCH}/#{REMOTE}/#{relative}"
      end

      def fetch_file(relative)
        url = URI.parse(remote_url(relative))
        raise 'Host de projeto nao autorizado.' unless url.host == 'raw.githubusercontent.com' && url.scheme == 'https' && url.port == 443
        max = relative == MANIFEST ? MAX_MANIFEST_BYTES : MAX_FILE_BYTES
        response = Net::HTTP.start(url.host, url.port, use_ssl: true, open_timeout: 8, read_timeout: 25) do |http|
          http.request(Net::HTTP::Get.new(url.request_uri, {'User-Agent'=>'MestreCAD-2021-Sync/1.3'}))
        end
        raise "GitHub retornou HTTP #{response.code} para #{relative}." unless response.is_a?(Net::HTTPSuccess)
        body = response.body.to_s.b
        raise "Arquivo #{relative} excede o limite de tamanho." if body.bytesize > max
        body
      end

      def validate_manifest!(data)
        raise 'Manifesto nao e JSON valido.' unless data.is_a?(Hash)
        raise 'Schema do manifesto nao suportado.' unless data['schema'] == SCHEMA
        raise 'Projeto do manifesto nao confere.' unless data['projeto'] == PROJECT
        raise 'Fonte sem SHA-256.' unless data['source_sha256'].to_s.match?(/\A[0-9a-f]{64}\z/)
        files = data['files']
        raise 'Lista de arquivos invalida.' unless files.is_a?(Hash) && files.keys.sort == FILES.sort
        FILES.each do |name|
          info = files[name]
          raise "Metadados invalidos: #{name}" unless info.is_a?(Hash)
          raise "SHA-256 invalido: #{name}" unless info['sha256'].to_s.match?(/\A[0-9a-f]{64}\z/)
          size = info['size']
          raise "Tamanho invalido: #{name}" unless size.is_a?(Integer) && size > 0 && size <= MAX_FILE_BYTES
        end
        true
      end

      def check_payloads!(manifest, files)
        validate_manifest!(manifest)
        raise 'Arquivos incompletos.' unless files.is_a?(Hash) && files.keys.sort == FILES.sort
        FILES.each do |name|
          payload = files.fetch(name)
          raise "Conteudo invalido: #{name}" unless payload.is_a?(String)
          info = manifest['files'].fetch(name)
          raise "Download incompleto: #{name}" unless payload.bytesize == info['size']
          raise "Checksum nao confere: #{name}" unless sha256(payload) == info['sha256']
        end
        raise 'SHA da fonte nao confere.' unless sha256(files['model.json']) == manifest['source_sha256']
        data = JSON.parse(files['model.json'])
        raise 'Projeto sem unidade mm.' unless data.is_a?(Hash) && data['unidades'] == 'mm' && data['schema'] == 'mestre-cad-geometria-v1'
        true
      end

      def fetch_package
        manifest_raw = fetch_file(MANIFEST)
        manifest = JSON.parse(manifest_raw)
        validate_manifest!(manifest)
        payloads = {}
        FILES.each { |name| payloads[name] = fetch_file(name) }
        check_payloads!(manifest, payloads)
        payloads[MANIFEST] = manifest_raw
        [manifest, payloads]
      end

      def assert_regular_paths!(root, relatives)
        raise 'Pasta do projeto e link simbolico.' if File.symlink?(root)
        relatives.each do |relative|
          nodes = relative.split('/')
          current = root
          nodes.each do |node|
            current = File.join(current, node)
            raise 'Um caminho local e link simbolico; sincronizacao recusada.' if File.symlink?(current)
          end
        end
      end

      def read_state(root)
        file = File.join(root, STATE)
        return nil unless File.file?(file)
        state = JSON.parse(File.read(file, encoding: 'UTF-8'))
        raise 'Estado de sincronizacao invalido.' unless state.is_a?(Hash) && state['schema'] == SCHEMA && state['files'].is_a?(Hash)
        state
      end

      def ensure_no_local_edits!(root, payloads, prior)
        payloads.each do |relative, content|
          dest = File.join(root, relative)
          next unless File.file?(dest)
          actual = sha256(File.binread(dest))
          next if actual == sha256(content)
          last = prior && prior['files'][relative]
          if last.nil? || !last.match?(/\A[0-9a-f]{64}\z/) || actual != last
            raise "Arquivo local alterado, mantido sem sobrescrita: #{relative}. Salve/renomeie sua copia antes de sincronizar."
          end
        end
      end

      # A parte transacional e testavel sem SketchUp ou rede.
      def apply_package!(manifest, payloads, root = local_root)
        files = payloads.reject { |k,_| k == MANIFEST }
        check_payloads!(manifest, files)
        raise 'Manifesto ausente do pacote.' unless payloads[MANIFEST].is_a?(String)
        raise 'Manifesto divergente.' unless JSON.parse(payloads[MANIFEST]) == manifest
        raise 'Caminhos de arquivos inesperados.' unless payloads.keys.sort == (FILES + [MANIFEST]).sort
        assert_regular_paths!(root, payloads.keys + [STATE])
        prior = read_state(root)
        ensure_no_local_edits!(root, payloads, prior)
        changes = payloads.select do |relative, bytes|
          dest = File.join(root,relative)
          !File.file?(dest) || File.binread(dest) != bytes
        end
        state = { 'schema'=>SCHEMA, 'projeto'=>PROJECT, 'updated_utc'=>Time.now.utc.iso8601,
                  'files'=>payloads.transform_values { |bytes| sha256(bytes) } }
        if prior && prior['files'] == state['files'] && changes.empty?
          return {changed: 0, root: root, backup: nil}
        end
        FileUtils.mkdir_p(root)
        backup = nil
        moved = []
        begin
          # Backups persistem se arquivos existentes forem substituidos.
          stamp = Time.now.utc.strftime('%Y%m%dT%H%M%SZ') + '-' + SecureRandom.hex(4)
          backup = File.join(root, 'backups', stamp)
          to_write = changes.merge(STATE => (JSON.pretty_generate(state) + "\n").b)
          to_write.each do |relative, bytes|
            dest = File.join(root, relative)
            FileUtils.mkdir_p(File.dirname(dest))
            assert_regular_paths!(root, [relative])
            original = File.file?(dest)
            if original
              saved = File.join(backup, relative)
              FileUtils.mkdir_p(File.dirname(saved))
              FileUtils.mv(dest, saved)
            end
            moved << [dest, original, File.join(backup, relative)]
            tmp = dest + '.mc-tmp-' + SecureRandom.hex(6)
            begin
              File.binwrite(tmp, bytes)
              FileUtils.mv(tmp, dest)
            ensure
              File.delete(tmp) if File.file?(tmp)
            end
          end
          {changed: changes.length, root: root, backup: (File.directory?(backup) ? backup : nil)}
        rescue StandardError
          moved.reverse_each do |dest, original, saved|
            File.delete(dest) if File.file?(dest)
            if original && File.file?(saved)
              FileUtils.mkdir_p(File.dirname(dest))
              FileUtils.mv(saved, dest)
            end
          end
          raise
        end
      end

      def sync_dialog
        raise 'Extensao requer SketchUp 2021.' unless Sketchup.version.to_i == 21
        question = "Sincronizar projeto #{PROJECT} do GitHub?\n" \
                   "Repositorio: #{REPO} / branch #{BRANCH}\n\n" \
                   "Arquivos CAD e geometria serao salvos em:\n#{local_root}\n\n" \
                   'Arquivos .SKP e alteracoes locais NAO serao sobrescritos.'
        return unless UI.messagebox(question, MB_YESNO) == IDYES
        manifest, payloads = fetch_package
        result = apply_package!(manifest, payloads)
        UI.messagebox("Sincronizacao concluida: #{result[:changed]} arquivo(s) novo(s)/atualizado(s).\n" \
                      "Local: #{result[:root]}\nRevisao: #{manifest['revisao']}\n\n" \
                      'Para gerar um SKP nativo, use Importar projeto sincronizado e Salvar como no SketchUp.')
        result
      rescue StandardError => e
        warn "MESTRE CAD SYNC ERRO: #{e.class}: #{e.message}"
        UI.messagebox("Sincronizacao nao concluida: #{e.message}\nOs arquivos locais foram preservados.")
        nil
      end

      def import_synced
        raise 'Extensao requer SketchUp 2021.' unless Sketchup.version.to_i == 21
        path = File.join(local_root, 'model.json')
        raise 'Projeto nao sincronizado. Execute Sincronizar arquivos CAD do GitHub primeiro.' unless File.file?(path)
        data = MestreCAD::SketchUp2021.read_json(path)
        MestreCAD::SketchUp2021.build(data)
      rescue StandardError => e
        warn "MESTRE CAD IMPORT ERRO: #{e.class}: #{e.message}"
        UI.messagebox("Importacao nao concluida: #{e.message}")
      end
    end
  end
end
