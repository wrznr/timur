# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class Sublexica:
  '''
  Extraction of relevant sublexica from the complete lexicon
  '''

  def __init__(self, syms):

    #
    # store alphabet
    self.__syms = syms

    self.__sigma_star = pynini.union(
        syms.characters,
        syms.categories,
        syms.stem_types,
        syms.origin_features,
        syms.inflection_classes,
        syms.geo_inflection_classes
        ).closure().optimize()

    self.__nodef_to_null = pynini.union(
        self.__sigma_star,
        syms.origin_features,
        pynini.transducer("<NoDef>", "", input_token_type=self.__syms.alphabet),
        syms.stem_types
        ).closure().optimize()

  def bdk_stems(self, lexicon):
    '''
    Base, derivation and compound stems (without derivation suffixes)
    '''
    return pynini.compose(
        lexicon,
        pynini.concat(
          pynini.concat(
            self.__syms.initial_features.closure(),
            pynini.string_map(["<Base_Stems>", "<Deriv_Stems>", "<Kompos_Stems>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
            ),
          self.__sigma_star
          )
        )

  def base_stems(self, lexicon):
    '''
    Base stems
    '''
    return pynini.compose(
      bdk_stems(lexicon, self.__syms.alphabet),
      pynini.concat(
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Base_Stems>", token_type=self.__syms.alphabet)
          ),
        self.__sigma_star
        )
      )

  def pref_stems(self, lexicon):
    '''
    Prefix stems
    '''
    return pynini.compose(
      lexicon,
      pynini.concat(
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.acceptor("<Pref_Stems>", token_type=self.__syms.alphabet)
          ),
        self.__sigma_star
        )
      )

  def verbal_pref_stems(self, lexicon):
    '''
    Verbal prefix stems
    '''
    return pynini.compose(
      pref_stems(lexicon, self.__syms.alphabet),
      pynini.concat(
        pynini.concat(
          pynini.concat(
            pynini.concat(
              self.__syms.initial_features.closure(),
              pynini.acceptor("<Pref_Stems>", token_type=self.__syms.alphabet)
              ),
            self.__sigma_star
            ),
          pynini.acceptor("<V>", token_type=self.__syms.alphabet)
          ),
        self.__sigma_star
        )
      )

  def simplex_suff_stems(self, lexicon):
    '''
    Derivation suffixes which combine with simplex stems
    '''
    return pynini.compose(
        lexicon,
        pynini.concat(
          pynini.concat(
            self.__syms.initial_features.closure(),
            pynini.concat(
              pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet),
              pynini.transducer("<simplex>", "", input_token_type=self.__syms.alphabet)
              ),
            ),
          self.__sigma_star
          )
        )

  def suff_deriv_suff_stems(self, lexicon):
    '''
    Derivation suffixes which combine with suffixed stems
    '''
    return pynini.compose(
        lexicon,
        pynini.concat(
          pynini.concat(
            self.__syms.initial_features.closure(),
            pynini.concat(
              pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet),
              pynini.transducer("<suffderiv>", "", input_token_type=self.__syms.alphabet)
              ),
            ),
          self.__sigma_star
          )
        )

  def pref_deriv_suff_stems(self, lexicon):
    '''
    Derivation suffixes which combine with prefixed stems
    '''
    return pynini.compose(
      lexicon,
      pynini.concat(
        pynini.concat(
          self.__syms.initial_features.closure(),
          pynini.concat(
              pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet),
              pynini.transducer("<prefderiv>", "", input_token_type=self.__syms.alphabet)
              ),
          ),
        self.__sigma_star
        )
      )

  def quant_suff_stems(self, lexicon):
    '''
    Derivation suffixes which combine with a number and a simplex stem
    '''
    return pynini.compose(
        lexicon,
        pynini.concat(
          pynini.concat(
            pynini.concat(
              pynini.concat(
                pynini.transducer("<QUANT>", "", input_token_type=self.__syms.alphabet),
                self.__syms.initial_features.closure()
                ),
              pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet)
              ),
            pynini.transducer("<simplex>", "", input_token_type=self.__syms.alphabet)
            ),
          self.__sigma_star
          )
        )
