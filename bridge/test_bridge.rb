# frozen_string_literal: true
# Testes offline: exercitam validacao e logica via mock, NAO substituem SketchUp real.
require 'minitest/autorun'
require 'json'
require 'tmpdir'
require 'minitest/mock'

class Numeric
  def mm; to_f / 25.4; end
  def to_mm; to_f * 25.4; end
end

IDYES = 6
MB_YESNO = 4

def file_loaded?(_path); false; end
def file_loaded(_path); true; end

module UI
  class Menu
    def add_submenu(_name); self; end
    def add_item(_name); true; end
    def add_separator; true; end
  end
  def self.menu(_name); Menu.new; end
  def self.messagebox(_msg, mode = nil); mode == MB_YESNO ? IDYES : 0; end
end

module Sketchup
  class FakePoint
    attr_reader :x, :y, :z
    def initialize(a); @x,@y,@z = a.map(&:to_f); end
  end
  class FakeBounds
    def initialize(points)
      @points = points
    end
    def valid?; !@points.empty?; end
    def min; FakePoint.new((0..2).map { |i| @points.map { |p| p[i] }.min }); end
    def max; FakePoint.new((0..2).map { |i| @points.map { |p| p[i] }.max }); end
  end
  class Face
    attr_reader :vertices
    def initialize(coords)
      @vertices = coords.map(&:dup)
      # SketchUp forces faces on the ground plane to point DOWN (-Z).
      @normal_z = coords.length >= 3 && coords.all? { |p| p[2].abs < 1e-9 } ? -1.0 : 1.0
    end
    def normal
      Struct.new(:z).new(@normal_z)
    end
    def reverse!
      @normal_z *= -1.0
      self
    end
    def pushpull(height)
      @vertices += @vertices.map { |p| [p[0],p[1],p[2]+height * @normal_z] }
      # Simula seis superficies geradas por PushPull
      @entities.add_faces_virtual(5)
    end
    def attach_owner(entities)
      @entities = entities
    end
  end
  class Entities
    def initialize
      @groups=[]
      @faces=[]
    end
    def add_group
      group = Group.new
      @groups << group
      group
    end
    def add_face(pts)
      face = Face.new(pts)
      face.attach_owner(self)
      @faces << face
      face
    end
    def add_faces_virtual(n)
      n.times { @faces << Face.new([]) }
    end
    def grep(klass)
      (@groups+@faces).grep(klass)
    end
    def all_points
      @faces.flat_map(&:vertices) + @groups.flat_map { |g| g.entities.all_points }
    end
    def groups; @groups; end
  end
  class Group
    attr_accessor :name, :layer
    attr_reader :entities
    def initialize
      @entities = Entities.new
      @attrs = Hash.new { |h,k| h[k] = {} }
    end
    def set_attribute(d,k,v); @attrs[d][k] = v; end
    def get_attribute(d,k); @attrs[d][k]; end
    def bounds; FakeBounds.new(@entities.all_points); end
  end
  class Layers < Hash
    def add(name); self[name] = name; end
  end
  class Selection < Array
    def add(entity); self << entity; end
  end
  class Model
    attr_reader :entities, :layers, :selection, :history
    def initialize
      @entities = Entities.new
      @layers = Layers.new
      @selection = Selection.new
      @history = []
    end
    def start_operation(*_args); @history << :start; end
    def commit_operation; @history << :commit; end
    def abort_operation; @history << :abort; end
    def path; 'C:/outro-projeto/meu-trabalho.skp'; end
    def save_copy(filename)
      raise 'Sobrescrita de SKP nao autorizada' if File.exist?(filename)
      File.binwrite(filename, "SKP_SIMULADO_2021\x00".b)
      @history << :save_copy
      true
    end
  end
  def self.version; '21.1.332'; end
  def self.active_model; @model ||= Model.new; end
  def self.reset; @model = Model.new; end
end

$LOADED_FEATURES << 'sketchup.rb'
require_relative 'mestre_cad_2021/core'

class TestMestreCAD < Minitest::Test
  PATH = File.expand_path('../examples/projeto-oficina-4x6-R00.json', __dir__)
  def setup
    Sketchup.reset
    @data = JSON.parse(File.read(PATH))
  end
  def test_import_synced_builds_audits_and_saves_native_skp_copy
    Dir.mktmpdir do |local|
      source=File.join(local,'model.json')
      File.binwrite(source,File.binread(PATH))
      ps=MestreCAD::SketchUp2021::ProjectSync
      ps.stub(:local_root,local) do
        dest=ps.import_synced
        assert File.file?(dest), 'SKP deveria ser salvo automaticamente'
        assert_match(/\.skp\z/,dest)
        assert_equal "SKP_SIMULADO_2021\x00".b,File.binread(dest)
        assert_equal 'C:/outro-projeto/meu-trabalho.skp',Sketchup.active_model.path
        assert_equal [:start,:commit,:save_copy],Sketchup.active_model.history
        assert_equal 1,Sketchup.active_model.entities.groups.length
      end
    end
  end

  def test_cancelled_import_does_not_create_sketchup_copy
    Dir.mktmpdir do |local|
      source=File.join(local,'model.json')
      File.binwrite(source,File.binread(PATH))
      ps=MestreCAD::SketchUp2021::ProjectSync
      original_messagebox=UI.method(:messagebox)
      UI.stub(:messagebox,lambda { |msg,mode=nil| mode==MB_YESNO ? 7 : original_messagebox.call(msg,mode) }) do
        ps.stub(:local_root,local) do
          assert_nil ps.import_synced
          assert_empty Dir.glob(File.join(local,'sketchup','*.skp'))
          assert_empty Sketchup.active_model.entities.groups
        end
      end
    end
  end

  def test_save_selected_existing_project_copy_without_reimport
    Dir.mktmpdir do |local|
      source=File.join(local,'model.json')
      File.binwrite(source,File.binread(PATH))
      root=MestreCAD::SketchUp2021.build(@data)
      ps=MestreCAD::SketchUp2021::ProjectSync
      ps.stub(:local_root,local) do
        file=ps.save_selected_skp
        assert File.file?(file)
        assert_equal 1,Sketchup.active_model.entities.groups.length
        assert_equal [:start,:commit,:save_copy],Sketchup.active_model.history
      end
    end
  end

  def test_example_contract
    result = MestreCAD::SketchUp2021.validate!(@data)
    assert_match(/PASS: 6 elementos/, result)
  end
  def test_creates_editable_groups_and_audits
    model = Sketchup.active_model
    preexisting = model.entities.add_group
    preexisting.name = 'Original nao alterar'
    root = MestreCAD::SketchUp2021.build(@data)
    assert_equal 2, model.entities.groups.size
    assert_equal 'Original nao alterar', preexisting.name
    assert_equal 6, root.entities.groups.size
    assert_equal [:start, :commit], model.history
    ok, issues, details = MestreCAD::SketchUp2021.verify_group(root)
    assert ok, "Auditoria inesperada: #{issues.join(', ')} (#{details})"
  end
  def test_ground_face_is_forced_down_in_sketchup
    face = Sketchup::Face.new([[0,0,0], [10,0,0], [10,10,0], [0,10,0]])
    assert_operator face.normal.z, :<, 0
  end
  def test_pillars_extrude_up_from_ground_plane
    root = MestreCAD::SketchUp2021.build(@data)
    p1 = root.entities.groups.find { |g| g.get_attribute('MestreCAD2021', 'id') == 'P1' }
    p3 = root.entities.groups.find { |g| g.get_attribute('MestreCAD2021', 'id') == 'P3' }
    assert_in_delta 0.0, p1.bounds.min.z.to_mm, 0.01
    assert_in_delta 3000.0, p1.bounds.max.z.to_mm, 0.01
    assert_in_delta 0.0, p3.bounds.min.z.to_mm, 0.01
    assert_in_delta 3413.0, p3.bounds.max.z.to_mm, 0.01
  end
  def test_box_above_ground_extrudes_up
    e = { 'id' => 'CX', 'nome' => 'teste', 'tipo' => 'caixa', 'tag' => 'TESTE',
          'origem_mm' => [0, 0, 1500], 'dimensoes_mm' => [200, 200, 500] }
    target = Sketchup.active_model.entities
    g = MestreCAD::SketchUp2021.add_element(target, e, Sketchup.active_model.layers)
    assert_in_delta 1500.0, g.bounds.min.z.to_mm, 0.01
    assert_in_delta 2000.0, g.bounds.max.z.to_mm, 0.01
  end
  def test_detects_dimension_change
    root = MestreCAD::SketchUp2021.build(@data)
    pillar = root.entities.groups.find { |g| g.get_attribute('MestreCAD2021', 'id') == 'P1' }
    pillar.entities.grep(Sketchup::Face).first.vertices[2][0] += 15.mm
    ok, issues, = MestreCAD::SketchUp2021.verify_group(root)
    refute ok
    assert issues.any? { |s| s.include?('P1') }
  end
  def test_rejects_non_coplanar_roof
    @data['elementos'][-1]['pontos_mm'][2][2] = 3410
    assert_raises(ArgumentError) { MestreCAD::SketchUp2021.validate!(@data) }
  end
  def test_rejects_outside_envelope
    @data['elementos'][1]['origem_mm'][0] = 3990
    assert_raises(ArgumentError) { MestreCAD::SketchUp2021.validate!(@data) }
  end
  def test_rejects_duplicate_id
    @data['elementos'][2]['id'] = 'P1'
    assert_raises(ArgumentError) { MestreCAD::SketchUp2021.validate!(@data) }
  end
  def test_rejects_wrong_unit
    @data['unidades'] = 'm'
    assert_raises(ArgumentError) { MestreCAD::SketchUp2021.validate!(@data) }
  end
  def test_rejects_commands_in_json
    @data['elementos'][1]['tipo'] = 'ruby_exec'
    assert_raises(ArgumentError) { MestreCAD::SketchUp2021.validate!(@data) }
  end
end
