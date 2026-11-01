# frozen_string_literal: true
# Testes offline para a atualizacao: NAO precisam do SketchUp real.
require 'minitest/autorun'
require 'tmpdir'
require 'digest'
require 'json'
require_relative 'mestre_cad_2021/updater'

IDYES = 6 unless defined?(IDYES)
MB_YESNO = 4 unless defined?(MB_YESNO)
module Sketchup
  def self.version; '21.1.332'; end
end
module UI
  def self.messagebox(_msg, _mode = nil); IDYES; end
end

class TestGithubUpdater < Minitest::Test
  UP = MestreCAD::SketchUp2021::Updater
  REPO = 'paulodepaula/mestre-cad-sketchup-2021'

  def asset_info(version: '1.4.1')
    name = "mestre-cad-bridge-2021-v#{version}.rbz"
    hash = 'a' * 64
    {
      'tag_name' => "v#{version}", 'draft' => false, 'prerelease' => false,
      'assets' => [{ 'name' => name, 'state' => 'uploaded', 'size' => 4500,
                     'digest' => "sha256:#{hash}",
                     'browser_download_url' => "https://github.com/#{REPO}/releases/download/v#{version}/#{name}" }]
    }
  end

  def test_version_order
    assert UP.version_newer?('v1.4.1')
    assert UP.version_newer?('v1.5.0')
    refute UP.version_newer?('v1.4.0')
    refute UP.version_newer?('v1.1.1')
    assert_raises(ArgumentError) { UP.version_newer?('v1.4.0-beta') }
  end

  def test_repository_validation
    assert_equal REPO, UP.valid_repository!(REPO)
    %w[https://github.com/x/y ../evil a/../../b someone\ repo a//b].each do |v|
      assert_raises(ArgumentError) { UP.valid_repository!(v) }
    end
  end

  def test_accepts_valid_release
    asset = UP.candidate_from_release(asset_info, REPO)
    assert_equal '1.4.1', asset[:version]
    assert_equal 'a'*64, asset[:sha256]
    assert_equal 4500, asset[:size]
  end

  def test_no_update_for_same_version
    assert_nil UP.candidate_from_release(asset_info(version: '1.4.0'), REPO)
  end

  def test_rejects_nonpublic_release
    data = asset_info
    data['prerelease'] = true
    assert_raises(ArgumentError) { UP.candidate_from_release(data, REPO) }
  end

  def test_rejects_foreign_asset_url
    data = asset_info
    data['assets'][0]['browser_download_url'] = 'https://evil.example/payload.rbz'
    assert_raises(RuntimeError) { UP.candidate_from_release(data, REPO) }
  end

  def test_rejects_asset_from_other_repo
    data = asset_info
    data['assets'][0]['browser_download_url'] = data['assets'][0]['browser_download_url'].sub(REPO, 'other/repository')
    assert_raises(RuntimeError) { UP.candidate_from_release(data, REPO) }
  end

  def test_rejects_missing_digest
    data = asset_info
    data['assets'][0].delete('digest')
    assert_raises(RuntimeError) { UP.candidate_from_release(data, REPO) }
  end

  def test_rejects_oversize_asset
    data = asset_info
    data['assets'][0]['size'] = UP::MAX_RBZ_BYTES + 1
    assert_raises(RuntimeError) { UP.candidate_from_release(data, REPO) }
  end

  def test_rejects_major_upgrade_without_manual_review
    data = asset_info(version: '2.0.0')
    assert_raises(RuntimeError) { UP.candidate_from_release(data, REPO) }
  end

  def test_sha256_verification_and_zip_signature
    Dir.mktmpdir('mestre-cad-test-') do |dir|
      path = File.join(dir, 'a.rbz')
      bytes = 'PK'.b + [3,4].pack('CC') + 'CONTEUDO_TESTE'.b
      File.binwrite(path, bytes)
      asset = {size: bytes.bytesize, sha256: Digest::SHA256.hexdigest(bytes)}
      assert UP.verify_archive!(path, asset)
      File.binwrite(path, bytes + 'TAMPERED')
      assert_raises(RuntimeError) { UP.verify_archive!(path, asset) }
    end
  end

  def test_backup_and_restore_last_installed_version
    Dir.mktmpdir('mestre-cad-backup-test-') do |temp|
      plugin_dir = File.join(temp, 'Plugins')
      backup_dir = File.join(temp, 'Backups')
      FileUtils.mkdir_p(File.join(plugin_dir, 'mestre_cad_2021'))
      File.write(File.join(plugin_dir, 'mestre_cad_2021.rb'), 'VERSION_OLD')
      File.write(File.join(plugin_dir, 'mestre_cad_2021', 'core.rb'), 'OLD_CODE')
      UP.stub(:plugins_path, plugin_dir) do
        UP.stub(:backup_base, backup_dir) do
          backup = UP.backup_current
          assert File.file?(File.join(backup, 'backup.json'))
          assert File.file?(File.join(backup, 'mestre_cad_2021', 'core.rb'))
          File.write(File.join(plugin_dir, 'mestre_cad_2021.rb'), 'VERSION_NEW')
          File.write(File.join(plugin_dir, 'mestre_cad_2021', 'core.rb'), 'NEW_CODE')
          UP.restore_previous
          assert_equal 'VERSION_OLD', File.read(File.join(plugin_dir, 'mestre_cad_2021.rb'))
          assert_equal 'OLD_CODE', File.read(File.join(plugin_dir, 'mestre_cad_2021', 'core.rb'))
        end
      end
    end
  end

  def test_integrity_must_match_sha256_even_for_zip_file
    Dir.mktmpdir('mestre-cad-checksum-test-') do |dir|
      path = File.join(dir, 'bad.rbz')
      data = 'PK'.b + [3,4].pack('CC') + 'SAFE'.b
      File.binwrite(path, data)
      asset = {size: data.bytesize, sha256: 'f'*64}
      assert_raises(RuntimeError) { UP.verify_archive!(path, asset) }
    end
  end

  def test_disallows_http_and_foreign_redirects
    %w[http://github.com/foo https://evil.example/foo https://github.com:8443/a].each do |u|
      assert_raises(RuntimeError) { UP.allowed_download_uri!(URI.parse(u)) }
    end
    assert UP.allowed_download_uri!(URI.parse('https://release-assets.githubusercontent.com/assets/abc'))
  end
end
