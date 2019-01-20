# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class DefaultsFst:
  '''
  Generation of default base, derivation and composition stems
  '''

  def __init__(self, syms):

    #
    # store alphabet
    self.__syms = syms
