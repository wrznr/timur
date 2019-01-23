# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols
from timur import fsts

class DefaultsFst:
  '''
  Generation of default base, derivation and composition stems
  '''

  def __init__(self, syms, sublexica, deko_filter, inflection):

    #
    # store alphabet
    self.__syms = syms


    #
    # run parts of morphology building (cf. timur_fst)
    #tmp = (sublexica.verbal_pref_stems + sublexica.base_stems) * sublexica.nodef_to_null * deko_filter.pref_filter
    tmp = (sublexica.base_stems)

    tmp.draw("def_tmp.dot", portrait=True)
