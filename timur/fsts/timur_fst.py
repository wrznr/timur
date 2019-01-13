# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini
import pickle

from pkg_resources import resource_stream, Requirement

from timur import symbols
from timur import helpers
from timur import fsts

class TimurFst:
  '''
  Put it all together
  '''

  def __init__(self):
    '''
    Constructor
    '''

    #
    # load the symbols
    self.__syms = symbols.Symbols(helpers.load_alphabet(resource_stream(Requirement.parse("timur"), 'timur/data/syms.txt')))

    #
    # empty fst
    self.__timur = None

  def __verify(self):
    '''
    Check whether timur is ready to roll
    '''
    return self.__timur is not None

  def lookup(self, string):
    '''
    Analyse a string
    '''
    result = []
    if self.__verify():
      string_acceptor = pynini.acceptor(" ".join(c for c in string), token_type=self.__syms.alphabet)
      result = list((string_acceptor * self.__timur).paths(input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).items())
    return result

  def load(self, fst):
    '''
    Load a previously built morphology
    '''
    self.__timur = pynini.Fst.read(fst)
    return self.__verify()

  def dumps(self):
    '''
    Print a previously built morphology
    '''
    if self.__verify():
      return self.__timur.text()
    return ""

  def dump(self, out_file):
    '''
    Save a previously built morphology
    '''
    if self.__verify():
      return self.__timur.write(out_file)
    return ""

  def build(self, lexicon_stream):
    '''
    Build the morphology from scratch
    '''
    lex = helpers.load_lexicon(lexicon_stream, self.__syms.alphabet)

    #
    # smor.fst
    #

    #
    # map.fst

    # include
    mappings = fsts.MapFst(self.__syms)

    # delete certain symbols on the upper and lower level
    lex = mappings.map1 * lex * mappings.map2

    #
    # num.fst

    # include
    #numericals = fsts.NumFst(self.__syms)

    # add the numeric stems to the other morphems
    # lex = lex | numericals.num_stems

    #
    # sublexica

    # sublexica.fst
    sublexica = fsts.Sublexica(self.__syms)

    # deko.fst
    #deko_filter = fsts.DekoFst(self.__syms)

    # flexion.fsts
    #inflection = fsts.InflectionFst(self.__syms)


    #
    # result
    self.__timur = lex
    return self.__verify()
