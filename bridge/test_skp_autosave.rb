# frozen_string_literal: true
# Auto-SKP tests: saving is driven by the real SketchUp API in the app.
# Here only file safety, validation and API call paths are simulated.
require 'minitest/autorun'
require 'minitest/mock'
require 'tmpdir'
require 'fileutils'
require 'json'
require_relative 'mestre_cad_2021/project_sync'

module MestreCAD
  module SketchUp2021
    def self.verify_group(group)
      group.audit
    end
  end
end

class TestSkpAutosave < Minitest::Test
  PS = MestreCAD::SketchUp2021::ProjectSync
  GroupMock = Struct.new(:stored, :audit_result) do
    def get_attribute(dict, key)
      return 'mestre-cad-geometria-v1' if dict == 'MestreCAD2021' && key == 'schema'
      return stored if dict == 'MestreCAD2021' && key == 'data'
      nil
    end
    def audit
      audit_result
    end
  end
  class ModelMock
    attr_reader :saved, :path, :calls
    attr_accessor :fail_copy, :empty_copy, :fail_save
    def initialize(path = 'C:/outro-projeto/existente.skp')
      @saved=[]
      @calls=[]
      @path=path
    end
    def save_copy(dest)
      @calls << [:save_copy, dest]
      raise 'Model must be saved before copying.' if @path.to_s.empty?
      @saved << dest
      File.binwrite(dest, @empty_copy ? '' : "SKP-PROVA-TESTE\x00")
      !@fail_copy
    end
    def save(dest)
      @calls << [:save, dest]
      File.binwrite(dest, @empty_copy ? '' : "SKP-PROVA-TESTE\x00")
      return false if @fail_save
      @path = dest
      @saved << dest
      true
    end
  end

  def fixture(root)
    json = File.join(root, 'model.json')
    payload = File.binread(File.join(__dir__,'mestre_cad_2021','exemplo-4x6.json'))
    File.binwrite(json, payload)
    [json, GroupMock.new(JSON.generate(JSON.parse(payload)), [true, [], 'PASS'])]
  end

  def test_saves_native_model_copy_in_local_project_without_changing_current_path
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      model = ModelMock.new
      path = PS.save_synced_skp!(model, group, source, root)
      assert_match(%r{/sketchup/obra-com-mezanino-R00-[a-f0-9]{12}-\d{8}T\d{6}Z-[a-f0-9]{8}\.skp\z}, path.tr('\\', '/'))
      assert_equal 'C:/outro-projeto/existente.skp', model.path
      assert_equal [path], model.saved
      assert_equal "SKP-PROVA-TESTE\x00", File.binread(path)
    end
  end

  def test_untitled_sketchup_2021_model_first_save_does_not_call_save_copy
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      model = ModelMock.new('')
      file = PS.save_synced_skp!(model, group, source, root)
      assert File.file?(file)
      assert_equal file, model.path
      assert_equal [[:save, file]], model.calls
    end
  end

  def test_after_initial_save_followup_creates_a_copy_without_changing_path
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      model = ModelMock.new('')
      first = PS.save_synced_skp!(model, group, source, root)
      File.binwrite(first, 'primeiro mantido')
      second = PS.save_synced_skp!(model, group, source, root)
      assert_equal first, model.path
      refute_equal first, second
      assert_equal [[:save,first], [:save_copy,second]], model.calls
      assert_equal 'primeiro mantido', File.binread(first)
      assert File.file?(second)
    end
  end

  def test_failed_first_save_removes_partial_file_but_not_other_project_files
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      model = ModelMock.new('')
      model.fail_save = true
      assert_raises(RuntimeError) { PS.save_synced_skp!(model, group, source, root) }
      assert_equal '', model.path
      assert_empty Dir.glob(File.join(root,'sketchup','*.skp'))
      assert File.file?(source)
    end
  end

  def test_repeated_save_never_overwrites_prior_skp
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      model = ModelMock.new
      first = PS.save_synced_skp!(model, group, source, root)
      File.binwrite(first, 'alterado localmente')
      second = PS.save_synced_skp!(model, group, source, root)
      refute_equal first, second
      assert_equal 'alterado localmente', File.binread(first)
      assert File.file?(second)
    end
  end

  def test_refuses_audited_failure
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      group.audit_result = [false, ['falha dimensional'], 'FAIL']
      model = ModelMock.new
      assert_raises(RuntimeError) { PS.save_synced_skp!(model,group,source,root) }
      assert_empty model.saved
    end
  end

  def test_refuses_tampered_json_after_import
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      File.binwrite(source,File.binread(source).sub('4000','4100'))
      model = ModelMock.new
      assert_raises(RuntimeError) { PS.save_synced_skp!(model,group,source,root) }
      assert_empty model.saved
    end
  end

  def test_refuses_unsafe_revision_filename
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      altered = JSON.parse(File.read(source))
      altered['revisao'] = '../evil'
      File.write(source, JSON.generate(altered))
      group.stored = JSON.generate(altered)
      model = ModelMock.new
      assert_raises(RuntimeError) { PS.save_synced_skp!(model,group,source,root) }
      assert_empty model.saved
    end
  end

  def test_failed_save_copy_cleans_partial_skp
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      model = ModelMock.new
      model.fail_copy=true
      assert_raises(RuntimeError) { PS.save_synced_skp!(model,group,source,root) }
      assert_empty Dir.glob(File.join(root,'sketchup','*.skp'))
    end
  end

  def test_empty_skp_copy_rejected
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      model = ModelMock.new
      model.empty_copy=true
      assert_raises(RuntimeError) { PS.save_synced_skp!(model,group,source,root) }
      assert_empty Dir.glob(File.join(root,'sketchup','*.skp'))
    end
  end

  def test_refuses_symlink_to_existing_folder
    Dir.mktmpdir do |root|
      source, group = fixture(root)
      Dir.mktmpdir do |other|
        File.symlink(other, File.join(root,'sketchup'))
        assert_raises(RuntimeError) { PS.save_synced_skp!(ModelMock.new,group,source,root) }
        assert_empty Dir.entries(other).reject { |n| n == '.' || n == '..' }
      end
    end
  end
end
