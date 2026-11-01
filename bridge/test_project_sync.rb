# frozen_string_literal: true
require 'minitest/autorun'
require 'tmpdir'
require 'json'
require 'digest'
require 'fileutils'
require_relative 'mestre_cad_2021/project_sync'

class TestProjectSync < Minitest::Test
  PS = MestreCAD::SketchUp2021::ProjectSync
  FIXTURE = File.join(__dir__, 'mestre_cad_2021', 'exemplo-4x6.json')

  def package
    payloads = {
      'model.json' => File.binread(FIXTURE),
      'cadcraft/planta.dxf' => "0\nSECTION\n2\nENTITIES\n0\nENDSEC\n0\nEOF\n".b,
      'cadcraft/elevacoes.dxf' => "0\nSECTION\n2\nENTITIES\n0\nENDSEC\n0\nEOF\n".b,
      'sketchup/modelo.dae' => '<COLLADA version="1.4.1"/>'.b
    }
    manifest = {
      'schema'=>PS::SCHEMA, 'projeto'=>PS::PROJECT, 'revisao'=>'R00',
      'source_sha256'=>PS.sha256(payloads['model.json']),
      'files'=>payloads.transform_values{|content| {'sha256'=>PS.sha256(content), 'size'=>content.bytesize}}
    }
    payloads['manifest.json']=(JSON.generate(manifest)+"\n").b
    [manifest,payloads]
  end

  def test_manifest_and_payload_valid
    manifest, files = package
    assert PS.validate_manifest!(manifest)
    assert PS.check_payloads!(manifest, files.reject { |k,_| k == 'manifest.json' })
  end

  def test_sync_then_idempotent_and_preserve_local_skp
    manifest, files = package
    Dir.mktmpdir do |root|
      skp_path=File.join(root, 'sketchup', 'meu-trabalho.skp')
      FileUtils.mkdir_p(File.dirname(skp_path))
      File.binwrite(skp_path, "MEU ARQUIVO SKP NAO TOCAR\x00".b)
      result=PS.apply_package!(manifest,files,root)
      assert_equal 5,result[:changed]
      assert_equal files['sketchup/modelo.dae'], File.binread(File.join(root,'sketchup','modelo.dae'))
      assert_equal "MEU ARQUIVO SKP NAO TOCAR\x00".b, File.binread(skp_path)
      result2=PS.apply_package!(manifest,files,root)
      assert_equal 0,result2[:changed]
      assert_nil result2[:backup]
    end
  end

  def test_rejects_local_modifications_without_overwriting
    manifest,files=package
    Dir.mktmpdir do |root|
      PS.apply_package!(manifest,files,root)
      file=File.join(root,'cadcraft/planta.dxf')
      File.write(file,'EDITADO PELO USUARIO')
      error=assert_raises(RuntimeError) { PS.apply_package!(manifest,files,root) }
      assert_match(/Arquivo local alterado/,error.message)
      assert_equal 'EDITADO PELO USUARIO',File.read(file)
    end
  end

  def test_does_not_overwrite_preexisting_unknown_local_file
    manifest,files=package
    Dir.mktmpdir do |root|
      FileUtils.mkdir_p(File.join(root,'cadcraft'))
      File.write(File.join(root,'cadcraft/planta.dxf'),'CLIENTE-ORIGINAL')
      assert_raises(RuntimeError) { PS.apply_package!(manifest,files,root) }
      assert_equal 'CLIENTE-ORIGINAL',File.read(File.join(root,'cadcraft/planta.dxf'))
    end
  end

  def test_rejects_modified_download_bytes_before_writing
    manifest, files=package
    files['cadcraft/planta.dxf']='X'+files['cadcraft/planta.dxf']
    Dir.mktmpdir do |root|
      assert_raises(RuntimeError) { PS.apply_package!(manifest,files,root) }
      refute File.exist?(File.join(root,'cadcraft/planta.dxf'))
    end
  end

  def test_rejects_extra_manifest_file_key
    manifest,files=package
    manifest['files']['../../evil.rb']={'sha256'=>'a'*64,'size'=>1}
    assert_raises(RuntimeError) { PS.validate_manifest!(manifest) }
  end

  def test_rejects_other_repo_paths
    %w[../../evil.rb sketchup/modelo.skp cadcraft/extrair.exe].each do |path|
      assert_raises(ArgumentError) { PS.remote_url(path) }
    end
    assert_match(%r{\Ahttps://raw.githubusercontent.com/paulodepaula/mestre-cad-sketchup-2021/main/projects/obra-com-mezanino/model.json\z},PS.remote_url('model.json'))
  end

  def test_prevent_symlink_overwrites
    manifest,files=package
    Dir.mktmpdir do |root|
      Dir.mktmpdir do |another|
        File.symlink(another,File.join(root,'cadcraft'))
        assert_raises(RuntimeError) { PS.apply_package!(manifest,files,root) }
      end
    end
  end

  def test_missing_source_sha_is_rejected
    manifest,files=package
    manifest['source_sha256']='0'*64
    assert_raises(RuntimeError) { PS.check_payloads!(manifest,files.reject{|k,_| k=='manifest.json'}) }
  end

  def test_changed_remote_creates_backup
    manifest,files=package
    Dir.mktmpdir do |root|
      PS.apply_package!(manifest,files,root)
      edited=files.dup
      # legitimate remote revision: source data is changed and manifest updated
      data=JSON.parse(edited['model.json'])
      data['nome']='Oficina revisada'
      edited['model.json']=(JSON.generate(data)+"\n").b
      changed_manifest=Marshal.load(Marshal.dump(manifest))
      changed_manifest['files']['model.json']['sha256']=PS.sha256(edited['model.json'])
      changed_manifest['files']['model.json']['size']=edited['model.json'].bytesize
      changed_manifest['source_sha256']=PS.sha256(edited['model.json'])
      edited['manifest.json']=(JSON.generate(changed_manifest)+"\n").b
      result=PS.apply_package!(changed_manifest,edited,root)
      assert_equal 2,result[:changed] # model + manifest
      assert File.directory?(result[:backup])
      assert_equal files['model.json'], File.binread(File.join(result[:backup],'model.json'))
    end
  end
end
