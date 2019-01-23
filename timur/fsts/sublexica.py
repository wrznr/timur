# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class Sublexica:
  '''
  Extraction of relevant sublexica from the complete lexicon
  '''

  def __init__(self, syms, lexicon):

    #
    # store alphabet
    self.__syms = syms

    #
    # store lexicon
    self.__lex = lexicon


    #
    # (private) helpers
    self.__sigma_star = pynini.union(
        syms.characters,
        syms.categories,
        syms.stem_types,
        syms.stem_type_features,
        syms.origin_features,
        syms.inflection_classes,
        syms.geo_inflection_classes
        ).closure().optimize()

    #
    # NoDef2NULL
    self.__nodef_to_null = pynini.union(
        self.__sigma_star,
        syms.origin_features,
        pynini.transducer("<NoDef>", "", input_token_type=self.__syms.alphabet),
        syms.stem_types
        ).closure().optimize()

    #
    # sublexica
    self.__bdk_stems = self.__construct_bdk_stems()
    self.__base_stems = self.__construct_base_stems()
    self.__pref_stems = self.__construct_pref_stems()
    self.__verbal_pref_stems = self.__construct_verbal_pref_stems()
    self.__simplex_suff_stems = self.__construct_simplex_suff_stems()
    self.__suff_deriv_suff_stems = self.__construct_suff_deriv_suff_stems()
    self.__pref_deriv_suff_stems = self.__construct_pref_deriv_suff_stems()
    self.__quant_suff_stems = self.__construct_quant_suff_stems()

  @property
  def nodef_to_null(self):
    '''
    Delete <NoDef> marker 
    '''
    return self.__nodef_to_null

  @property
  def bdk_stems(self):
    '''
    Return base, derivation and compound stems 
    '''
    return self.__bdk_stems

  @property
  def base_stems(self):
    '''
    Return base stems 
    '''
    return self.__base_stems

  @property
  def pref_stems(self):
    '''
    Return prefix stems 
    '''
    return self.__pref_stems

  @property
  def verbal_pref_stems(self):
    '''
    Return verbal prefix stems 
    '''
    return self.__verbal_pref_stems

  @property
  def simplex_suff_stems(self):
    '''
    Return simplex suffix stems 
    '''
    return self.__simplex_suff_stems

  @property
  def suff_deriv_suff_stems(self):
    '''
    Return suffix stems for previously suffixed words
    '''
    return self.__suff_deriv_suff_stems

  @property
  def pref_deriv_suff_stems(self):
    '''
    Return suffix stems for previously prefixed words
    '''
    return self.__pref_deriv_suff_stems

  @property
  def quant_suff_stems(self):
    '''
    Return suffix stems which combine with numericals
    '''
    return self.__quant_suff_stems

  def __construct_bdk_stems(self):
    '''
    Base, derivation and compound stems (without derivation suffixes)
    '''
    return pynini.compose(
        self.__lex,
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.string_map(["<Base_Stems>", "<Deriv_Stems>", "<Kompos_Stems>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
          self.__sigma_star
          )
        ).optimize()

  def __construct_base_stems(self):
    '''
    Base stems
    '''
    return pynini.compose(
        self.__bdk_stems,
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Base_Stems>", token_type=self.__syms.alphabet),
          self.__sigma_star
          )
        ).optimize()

  def __construct_pref_stems(self):
    '''
    Prefix stems
    '''
    return pynini.compose(
        self.__lex,
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Pref_Stems>", token_type=self.__syms.alphabet),
          self.__sigma_star
          )
        ).optimize()

  def __construct_verbal_pref_stems(self):
    '''
    Verbal prefix stems
    '''
    return pynini.compose(
        self.__pref_stems,
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Pref_Stems>", token_type=self.__syms.alphabet),
          self.__sigma_star,
          pynini.acceptor("<V>", token_type=self.__syms.alphabet),
          self.__sigma_star
          )
        ).optimize()

  def __construct_simplex_suff_stems(self):
    '''
    Derivation suffixes which combine with simplex stems
    '''
    return pynini.compose(
        self.__lex,
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet),
          pynini.transducer("<simplex>", "", input_token_type=self.__syms.alphabet),
          self.__sigma_star
          )
        ).optimize()

  def __construct_suff_deriv_suff_stems(self):
    '''
    Derivation suffixes which combine with suffixed stems
    '''
    return pynini.compose(
        self.__lex,
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet),
          pynini.transducer("<suffderiv>", "", input_token_type=self.__syms.alphabet),
          self.__sigma_star
          )
        ).optimize()

  def __construct_pref_deriv_suff_stems(self):
    '''
    Derivation suffixes which combine with prefixed stems
    '''
    return pynini.compose(
        self.__lex,
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet),
          pynini.transducer("<prefderiv>", "", input_token_type=self.__syms.alphabet),
          self.__sigma_star
          )
        ).optimize()

  def __construct_quant_suff_stems(self):
    '''
    Derivation suffixes which combine with a number and a simplex stem
    '''
    return pynini.compose(
        self.__lex,
        pynini.concat(
          pynini.transducer("<QUANT>", "", input_token_type=self.__syms.alphabet),
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet),
          pynini.transducer("<simplex>", "", input_token_type=self.__syms.alphabet),
          self.__sigma_star
          )
        ).optimize()
