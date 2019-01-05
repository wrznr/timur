# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class InflectionFst:
  '''
  Define the inflection paradigm
  '''

  def __init__(self,syms):

    #
    # store alphabet
    self.__syms = syms
