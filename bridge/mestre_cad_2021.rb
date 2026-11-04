# frozen_string_literal: true
# Carregador da extensao local Mestre CAD 2021 (SketchUp Desktop 21.x).
require 'sketchup.rb'
require 'extensions.rb'

module MestreCAD
  module SketchUp2021
    unless defined?(EXTENSION_REGISTERED)
      ext = SketchupExtension.new('Mestre CAD - Geometria 2021', 'mestre_cad_2021/core')
      ext.description = 'Importa, atualiza preservando acabamentos, audita geometria e sincroniza arquivos CAD do GitHub.'
      ext.version = '1.5.1'
      ext.creator = 'Mestre CAD & SketchUp 2021'
      Sketchup.register_extension(ext, true)
      EXTENSION_REGISTERED = true
    end
  end
end
