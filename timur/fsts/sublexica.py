# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur.helpers import union
from timur.helpers import concat

from timur.fsts import symbol_sets

def sigma_star(symbol_table):
  return pynini.union(
      symbol_sets.characters(symbol_table),
      symbol_sets.categories(symbol_table),
      symbol_sets.stem_types(symbol_table),
      symbol_sets.origin_features(symbol_table),
      symbol_sets.inflection_classes(symbol_table),
      symbol_sets.geo_inflection_classes(symbol_table)
      ).closure()

def nodef_to_null(symbol_table):
  return pynini.union(
      sigma_star(symbol_table),
      symbol_sets.origin_features(symbol_table),
      pynini.transducer("<NoDef>", "", input_token_type=symbol_table),
      symbol_sets.stem_types(symbol_table)
      ).closure()

def bdk_stems(lexicon, symbol_table):
  '''
  Base, derivation and compound stems (without derivation suffixes)
  '''
  return pynini.compose(
      lexicon,
      pynini.concat(
        pynini.concat(
          symbol_sets.initial_features(symbol_table).closure(),
          pynini.string_map(["<Base_Stems>", "<Deriv_Stems>", "<Kompos_Stems>"], input_token_type=symbol_table, output_token_type=symbol_table)
          ),
        sigma_star(symbol_table)
        )
      )

def base_stems(lexicon, symbol_table):
    '''
    Base stems
    '''
    return pynini.compose(
      bdk_stems(lexicon, symbol_table),
      pynini.concat(
        pynini.concat(
          symbol_sets.initial_features(symbol_table).closure(),
          pynini.acceptor("<Base_Stems>", token_type=symbol_table)
          ),
        sigma_star(symbol_table)
        )
      )

def pref_stems(lexicon, symbol_table):
    '''
    Prefix stems
    '''
    return pynini.compose(
      lexicon,
      pynini.concat(
        pynini.concat(
          symbol_sets.initial_features(symbol_table).closure(),
          pynini.acceptor("<Pref_Stems>", token_type=symbol_table)
          ),
        sigma_star(symbol_table)
        )
      )