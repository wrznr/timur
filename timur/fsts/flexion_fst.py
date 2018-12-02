# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur.helpers import union
from timur.helpers import concat

from timur.fsts import symbol_sets

class Flexion:
  '''
  Define the inflection paradigm
  '''

  def __init__(self):
    self.data = []
