# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur.helpers import union
from timur.helpers import concat

from timur.fsts import symbol_sets

def tail(symbol_table):

  # C1
  initial_stuff = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>", "<Pref_Stems>"], input_token_type=symbol_table, output_token_type=symbol_table)
      ).closure()
  # C2
  intermediate_stuff = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<Suff_Stems>"], input_token_type=symbol_table, output_token_type=symbol_table)
      ).closure()

  # C3
  final_stuff = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>"], input_token_type=symbol_table, output_token_type=symbol_table),
      symbol_sets.categories(symbol_table),
      symbol_sets.stem_type_features(symbol_table),
      symbol_sets.origin_features(symbol_table),
      pynini.string_map(["<NSNeut_es_e>", "<NSFem_0_n>", "<NSFem_0_en>", "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>"], input_token_type=symbol_table, output_token_type=symbol_table)
      ).closure()

  # TAIL
  return pynini.concat(
      pynini.concat(
        initial_stuff,
        pynini.concat(
          symbol_sets.base_stem_types(symbol_table),
          intermediate_stuff
          )
        ).closure(0,1),
      pynini.concat(
        final_stuff,
        symbol_sets.inflection_classes(symbol_table).closure(0,1)
        )
      )
