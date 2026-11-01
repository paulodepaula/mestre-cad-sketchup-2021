# frozen_string_literal: true
# Mestre CAD 2021 - atualizador por GitHub Releases (SketchUp 21.x, Ruby 2.7).
# Executa somente mediante clique e confirmacao do usuario.
# Nao baixa ou executa scripts arbitrarios do branch main.
require 'json'
require 'net/http'
require 'uri'
require 'digest'
require 'tmpdir'
require 'fileutils'
require 'securerandom'
require 'time'

module MestreCAD
  module SketchUp2021
    module Updater
      extend self

      VERSION = '1.4.0'.freeze
      DEFAULT_REPOSITORY = 'paulodepaula/mestre-cad-sketchup-2021'.freeze
      SETTINGS_KEY = 'MestreCAD2021'.freeze
      MAX_RBZ_BYTES = 20 * 1024 * 1024
      MAX_RELEASE_BYTES = 1024 * 1024
      ALLOWED_DOWNLOAD_HOSTS = %w[
        github.com
        release-assets.githubusercontent.com
        objects.githubusercontent.com
      ].freeze

      def version_tuple(value)
        match = /\Av?(\d{1,4})\.(\d{1,4})\.(\d{1,4})\z/.match(value.to_s)
        raise ArgumentError, "Versao invalida: #{value.inspect}" unless match
        match.captures.map(&:to_i)
      end

      def version_newer?(remote, local = VERSION)
        (version_tuple(remote) <=> version_tuple(local)) == 1
      end

      def valid_repository!(value)
        value = value.to_s.strip
        valid = value.match?(/\A[A-Za-z0-9][A-Za-z0-9_.-]*\/[A-Za-z0-9][A-Za-z0-9_.-]*\z/)
        valid &&= !value.include?('..') && !value.include?('--')
        raise ArgumentError, 'Informe usuario/repositorio, sem URL, espacos ou caminhos extras.' unless valid
        value
      end

      def repository
        value = Sketchup.read_default(SETTINGS_KEY, 'GitHubRepository', DEFAULT_REPOSITORY)
        valid_repository!(value)
      end

      def configure_repository
        old = repository
        response = UI.inputbox(['Repositorio publico GitHub (usuario/repositorio):'], [old], 'Mestre CAD - GitHub')
        return unless response
        chosen = valid_repository!(response.first)
        Sketchup.write_default(SETTINGS_KEY, 'GitHubRepository', chosen)
        UI.messagebox("Repositorio configurado: #{chosen}\nUse Verificar atualizacoes no GitHub.")
      rescue StandardError => e
        UI.messagebox("Nao foi possivel configurar GitHub: #{e.message}")
      end

      def require_sketchup_2021!
        raise 'Este atualizador requer SketchUp Desktop 2021 (21.x).' unless Sketchup.version.to_i == 21
      end

      def github_release_url(repo)
        URI.parse("https://api.github.com/repos/#{valid_repository!(repo)}/releases/latest")
      end

      def fetch_latest_release(repo)
        uri = github_release_url(repo)
        response = Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 8, read_timeout: 15) do |http|
          req = Net::HTTP::Get.new(uri.request_uri)
          req['Accept'] = 'application/vnd.github+json'
          req['User-Agent'] = "MestreCAD-SketchUp2021/#{VERSION}"
          http.request(req)
        end
        case response.code.to_i
        when 200
          raise 'Resposta GitHub muito grande.' if response.body.to_s.bytesize > MAX_RELEASE_BYTES
          data = JSON.parse(response.body)
          raise 'Resposta GitHub invalida.' unless data.is_a?(Hash)
          data
        when 404
          raise "Repositorio #{repo} sem release publica (ou inexistente). Crie o repositorio e publique uma versao."
        when 403
          raise 'Consulta GitHub bloqueada ou limitada (HTTP 403); tente novamente mais tarde.'
        else
          raise "GitHub indisponivel (HTTP #{response.code})."
        end
      end

      def candidate_from_release(release, repo)
        raise ArgumentError, 'Release invalida.' unless release.is_a?(Hash)
        raise ArgumentError, 'Release de rascunho ou pre-release nao permitida.' if release['draft'] || release['prerelease']
        tag = release['tag_name'].to_s
        version_tuple(tag)
        return nil unless version_newer?(tag)
        version = tag.sub(/\Av/, '')
        # Evita atualizacoes para extensoes com formato major desconhecido.
        raise 'Atualizacao de major version exige instalacao supervisionada.' unless version_tuple(tag)[0] == version_tuple(VERSION)[0]
        expected_name = "mestre-cad-bridge-2021-v#{version}.rbz"
        asset = Array(release['assets']).find { |item| item.is_a?(Hash) && item['name'] == expected_name }
        raise "Release #{tag} sem o instalador #{expected_name}." unless asset
        raise 'Asset nao finalizado.' unless asset['state'] == 'uploaded'
        size = asset['size']
        raise 'Tamanho de arquivo invalido.' unless size.is_a?(Integer) && size > 0 && size <= MAX_RBZ_BYTES
        match = /\Asha256:([a-f0-9]{64})\z/i.match(asset['digest'].to_s)
        raise 'Release sem digest SHA-256 valido.' unless match
        raw_url = asset['browser_download_url'].to_s
        uri = URI.parse(raw_url)
        path = "/#{valid_repository!(repo)}/releases/download/#{tag}/#{expected_name}"
        raise 'URL do asset nao corresponde ao repositorio autorizado.' unless uri.scheme == 'https' && uri.host == 'github.com' && uri.userinfo.nil? && uri.port == 443 && uri.path == path
        { version: version, tag: tag, name: expected_name, url: uri.to_s,
          sha256: match[1].downcase, size: size }
      end

      def allowed_download_uri!(uri)
        raise 'Protocolo de download nao permitido.' unless uri.scheme == 'https'
        raise 'Redirecionamento para host nao autorizado.' unless ALLOWED_DOWNLOAD_HOSTS.include?(uri.host)
        raise 'Credenciais embutidas na URL nao permitidas.' unless uri.userinfo.nil?
        raise 'Porta de download nao permitida.' unless uri.port == 443
        uri
      end

      def download_file(url, destination)
        uri = URI.parse(url)
        redirects = 0
        downloaded = 0
        loop do
          allowed_download_uri!(uri)
          next_uri = nil
          Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 8, read_timeout: 30) do |http|
            request = Net::HTTP::Get.new(uri.request_uri)
            request['User-Agent'] = "MestreCAD-SketchUp2021/#{VERSION}"
            request['Accept'] = 'application/octet-stream'
            http.request(request) do |response|
              case response
              when Net::HTTPRedirection
                location = response['location'].to_s
                raise 'Redirecionamento sem endereco.' if location.empty?
                next_uri = URI.join(uri.to_s, location)
              when Net::HTTPSuccess
                File.open(destination, 'wb') do |out|
                  response.read_body do |chunk|
                    downloaded += chunk.bytesize
                    raise 'Download excedeu limite de tamanho.' if downloaded > MAX_RBZ_BYTES
                    out.write(chunk)
                  end
                end
              else
                raise "Falha ao baixar pacote: HTTP #{response.code}."
              end
            end
          end
          return downloaded unless next_uri
          redirects += 1
          raise 'Excesso de redirecionamentos no download.' if redirects > 5
          uri = next_uri
        end
      end

      def verify_archive!(path, asset)
        size = File.size(path)
        raise "Arquivo incompleto: #{size} bytes, esperado #{asset[:size]}." unless size == asset[:size]
        hash = Digest::SHA256.file(path).hexdigest
        raise 'SHA-256 nao confere: pacote recusado.' unless hash == asset[:sha256]
        raise 'O arquivo nao parece ser um RBZ/ZIP.' unless File.binread(path, 4).bytes == [0x50, 0x4b, 0x03, 0x04]
        true
      end

      def plugins_path
        path = Sketchup.find_support_file('Plugins')
        raise 'Pasta de extensoes do SketchUp nao encontrada.' unless path.is_a?(String) && File.directory?(path)
        path
      end

      def backup_base
        base = ENV['APPDATA'] || File.join(Dir.home, '.local', 'share')
        File.join(base, 'MestreCAD2021', 'backups')
      end

      def backup_current
        installed = plugins_path
        root = File.join(installed, 'mestre_cad_2021.rb')
        folder = File.join(installed, 'mestre_cad_2021')
        raise 'Extensao atual nao foi encontrada para backup.' unless File.file?(root) && File.directory?(folder)
        FileUtils.mkdir_p(backup_base)
        name = "v#{VERSION}-#{Time.now.utc.strftime('%Y%m%dT%H%M%SZ')}-#{SecureRandom.hex(3)}"
        dest = File.join(backup_base, name)
        FileUtils.mkdir_p(dest)
        FileUtils.cp(root, File.join(dest, 'mestre_cad_2021.rb'))
        FileUtils.cp_r(folder, File.join(dest, 'mestre_cad_2021'))
        File.write(File.join(dest, 'backup.json'), JSON.pretty_generate({ 'version' => VERSION, 'created_utc' => Time.now.utc.iso8601 }))
        dest
      end

      def list_backups
        Dir.glob(File.join(backup_base, '*')).select do |folder|
          File.directory?(folder) &&
            File.file?(File.join(folder, 'backup.json')) &&
            File.file?(File.join(folder, 'mestre_cad_2021.rb')) &&
            File.directory?(File.join(folder, 'mestre_cad_2021'))
        end.sort
      end

      def restore_previous
        require_sketchup_2021!
        backup = list_backups.last
        raise 'Nao existe copia anterior. Use o instalador RBZ manual.' unless backup
        yes = UI.messagebox("Restaurar os arquivos da ultima copia?\n#{File.basename(backup)}\n\nSalve seu modelo. Reinicie o SketchUp depois.", MB_YESNO)
        return unless yes == IDYES
        plugin_dir = plugins_path
        current_root = File.join(plugin_dir, 'mestre_cad_2021.rb')
        current_folder = File.join(plugin_dir, 'mestre_cad_2021')
        # Preserva a versao atual antes de tentar o restauro.
        snapshot = Dir.mktmpdir('mestre-cad-pre-restauro-')
        begin
          FileUtils.cp(current_root, snapshot) if File.file?(current_root)
          FileUtils.cp_r(current_folder, snapshot) if File.directory?(current_folder)
          FileUtils.cp(File.join(backup, 'mestre_cad_2021.rb'), current_root)
          FileUtils.rm_rf(current_folder)
          FileUtils.cp_r(File.join(backup, 'mestre_cad_2021'), current_folder)
          UI.messagebox('Copia anterior restaurada. Reinicie o SketchUp para ativar.')
        rescue StandardError => e
          begin
            saved_root = File.join(snapshot, 'mestre_cad_2021.rb')
            saved_folder = File.join(snapshot, 'mestre_cad_2021')
            FileUtils.cp(saved_root, current_root) if File.file?(saved_root)
            if File.directory?(saved_folder)
              FileUtils.rm_rf(current_folder)
              FileUtils.cp_r(saved_folder, current_folder)
            end
          rescue StandardError => restore_error
            warn "MESTRE CAD RESTORE FALHA: #{restore_error.message}; copia em #{snapshot}"
            snapshot = nil
          end
          raise "Restauro falhou: #{e.message}."
        ensure
          FileUtils.remove_entry(snapshot) if snapshot && File.directory?(snapshot)
        end
      rescue StandardError => e
        warn "MESTRE CAD UPDATE ERRO: #{e.class} - #{e.message}"
        UI.messagebox(e.message)
      end

      def check_for_updates
        require_sketchup_2021!
        repo = repository
        release = fetch_latest_release(repo)
        asset = candidate_from_release(release, repo)
        unless asset
          UI.messagebox("Mestre CAD #{VERSION} - nenhuma versao mais recente no GitHub.\nRepositorio: #{repo}")
          return
        end
        question = "Mestre CAD #{VERSION} -> #{asset[:version]}\n" \
                   "Repositorio: #{repo}\nArquivo: #{asset[:name]}\n" \
                   "Tamanho: #{asset[:size]} bytes\nSHA-256: #{asset[:sha256][0, 12]}...\n\n" \
                   "O pacote sera verificado e a versao atual sera salva.\n" \
                   "Salve seu projeto antes. Instalar esta atualizacao?"
        return unless UI.messagebox(question, MB_YESNO) == IDYES
        Dir.mktmpdir('mestre-cad-download-') do |dir|
          path = File.join(dir, asset[:name])
          download_file(asset[:url], path)
          verify_archive!(path, asset)
          backup = backup_current
          begin
            result = Sketchup.install_from_archive(path, true)
            raise 'SketchUp nao concluiu a instalacao.' unless result
          rescue Interrupt
            UI.messagebox("Instalacao cancelada. Backup preservado em:\n#{backup}")
            return
          end
          UI.messagebox("Atualizacao instalada!\n#{VERSION} -> #{asset[:version]}\nBackup: #{backup}\n\nReinicie o SketchUp antes de usar a nova versao.")
        end
      rescue StandardError => e
        warn "MESTRE CAD UPDATE ERRO: #{e.class}: #{e.message}"
        UI.messagebox("Atualizacao nao concluida: #{e.message}\nNenhum projeto SKP foi modificado pelo atualizador.")
      end
    end
  end
end
