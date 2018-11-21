# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur.helpers import union
from timur.helpers import concat

from timur.fsts import symbol_sets

def suff_stems_filter(features, symbol_table):
  '''
  Return a union over filters for each feature given
  '''
  filtering = pynini.Fst()
  filtering.set_input_symbols(symbol_table)
  filtering.set_output_symbols(symbol_table)
  suff_stems = pynini.acceptor("<Suff_Stems>", token_type=symbol_table)
  for feature in features:
    to_eps = pynini.transducer(feature, "", input_token_type=symbol_table)
    filtering = pynini.union(
        filtering,
        pynini.concat(
          pynini.concat(
            to_eps,
            suff_stems
            ),
          to_eps
          )
        )
  return filtering

def tail(symbol_table):
  '''
  Define possible final sequences of a derivation
  '''

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

def origin_filter(symbol_table):
  '''
  Filter-out non-matching origin feature sequences
  '''

  alphabet = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=symbol_table, output_token_type=symbol_table),
      symbol_sets.stem_types(symbol_table),
      symbol_sets.categories(symbol_table),
      symbol_sets.stem_type_features(symbol_table)
      ).closure()

  filtering = suff_stems_filter(["<nativ>", "<frei>", "<gebunden>", "<kurz>", "<lang>", "<fremd>", "<klassisch>", "<NSNeut_es_e>", "<NSFem_0_n>", "<NSFem_0_en>", "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>", "<NGeo-$isch-Adj+>", "<NGeo-0-Name-Fem_0>", "<NGeo-0-Name-Masc_s>", "<NGeo-0-Name-Neut_s>", "<NGeo-a-Name-Fem_s>", "<NGeo-a-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-aner-Adj0-Up>", "<NGeo-anisch-Adj+>", "<NGeo-e-NMasc_n_n>", "<NGeo-e-Name-Fem_0>", "<NGeo-e-Name-Neut_s>", "<NGeo-ei-Name-Fem_0>", "<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>", "<NGeo-0-NMasc_s_0>", "<NGeo-0-Adj0-Up>", "<NGeo-erisch-Adj+>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>", "<NGeo-ien-Name-Neut_s>", "<NGeo-ier-NMasc_s_0>", "<NGeo-isch-Adj+>", "<NGeo-istan-Name-Neut_s>", "<NGeo-land-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-ner-Adj0-Up>", "<NGeo-nisch-Adj+>"], symbol_table).optimize()

  return pynini.concat(
      pynini.concat(
        alphabet,
        filtering
        ).closure(),
      tail(symbol_table)
      )

def stem_type_filter(symbol_table):
  '''
  Filter-out non-matching stem type sequences
  '''

  alphabet = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=symbol_table, output_token_type=symbol_table),
      symbol_sets.stem_types(symbol_table),
      symbol_sets.categories(symbol_table),
      ).closure()

  filtering = suff_stems_filter(["<deriv>", "<kompos>"], symbol_table).optimize()

  return pynini.concat(
      pynini.concat(
        alphabet,
        filtering
        ).closure(),
      tail(symbol_table)
      )

def category_filter(symbol_table):
  '''
  Filter-out non-matching category sequences
  '''

  alphabet = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=symbol_table, output_token_type=symbol_table),
      symbol_sets.stem_types(symbol_table),
      symbol_sets.categories(symbol_table),
      ).closure()

  filtering = suff_stems_filter(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>"], symbol_table).optimize()

  return pynini.concat(
      pynini.concat(
        alphabet,
        filtering
        ).closure(),
      tail(symbol_table)
      )

def umlautung(symbol_table):
  '''
  Map "a", "o" and "u" onto "ä", "ö" and "ü", corresp., if the umlaut marker "<UL>" is present.
  '''

  alphabet = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=symbol_table, output_token_type=symbol_table),
      symbol_sets.stem_types(symbol_table),
      symbol_sets.categories(symbol_table),
      ).closure()

  return pynini.concat(
      pynini.concat(
        alphabet,
        pynini.concat(
          symbol_sets.consonants(symbol_table),
          pynini.concat(
            pynini.union(
              pynini.union(
                pynini.transducer("a", "ä", input_token_type=symbol_table, output_token_type=symbol_table),
                pynini.transducer("o", "ö", input_token_type=symbol_table, output_token_type=symbol_table),
                pynini.transducer("u", "ü", input_token_type=symbol_table, output_token_type=symbol_table)
                ),
              pynini.concat(
                pynini.transducer("a", "ä", input_token_type=symbol_table, output_token_type=symbol_table),
                pynini.union(
                  pynini.transducer("a", "", input_token_type=symbol_table),
                  pynini.acceptor("u", token_type=symbol_table)
                  )
                )
              ),
            pynini.concat(
              symbol_sets.consonants(symbol_table).closure(),
              pynini.concat(
                pynini.concat(
                  pynini.acceptor("e", token_type=symbol_table),
                  pynini.string_map(["l", "r"], input_token_type=symbol_table, output_token_type=symbol_table)
                  ).closure(0, 1),
                pynini.concat(
                  pynini.acceptor("<Suff_Stems>", token_type=symbol_table),
                  pynini.transducer("<UL>", "", input_token_type=symbol_table)
                  )
                )
              )
            )
          ).closure(0, 1)
        ),
      tail(symbol_table)
      )

def suff_phon(symbol_table):
  '''
  '''

  alphabet = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>", "<NN>", "<ADJ>"], input_token_type=symbol_table, output_token_type=symbol_table),
      symbol_sets.stem_types(symbol_table),
      ).closure()

  return pynini.concat(
      pynini.cdrewrite(
        pynini.transducer("i", "", input_token_type=symbol_table),
        pynini.concat(
          pynini.union(
            pynini.acceptor("i", token_type=symbol_table),
            pynini.concat(
              symbol_sets.consonants(symbol_table),
              pynini.acceptor("y", token_type=symbol_table)
              )
            ),
          pynini.acceptor("<Suff_Stems>", token_type=symbol_table)
          ),
        "",
        alphabet
        ),
      tail(symbol_table)
      )

def suffix_filter(symbol_table):
  '''
  Construct the complete suffix filter 
  '''

  suff_filter = pynini.compose(
      origin_filter(symbol_table),
      pynini.compose(
        stem_type_filter(symbol_table),
        pynini.compose(
          category_filter(symbol_table),
          umlautung(symbol_table)
          )
        )
      )
  return pynini.compose(suff_filter, suff_phon(symbol_table))

def prefix_filter(symbol_table):
  '''
  Construct the (complete) prefix filter
  '''

  alphabet = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=symbol_table, output_token_type=symbol_table),
      symbol_sets.stem_types(symbol_table),
      symbol_sets.categories(symbol_table),
      ).closure()

  # delete <ge> at certain suffixes like 'ver'
  del_ge = pynini.concat(
      pynini.transducer("<no-ge>", "", input_token_type=symbol_table),
      pynini.concat(
        pynini.acceptor("<Pref_Stems>", token_type=symbol_table),
        pynini.concat(
          pynini.union(
            symbol_sets.characters(symbol_table),
            pynini.string_map(["<n>", "<e>", "<d>", "<~n>"])
            ).closure(),
          pynini.concat(
            pynini.transducer(
              pynini.concat(pynini.acceptor("<V>", token_type=symbol_table), pynini.acceptor("<nativ>", token_type=symbol_table)),
              ""
              ),
            pynini.concat(
              pynini.acceptor("<NoDef>", token_type=symbol_table).closure(0, 1),
              pynini.concat(
                pynini.transducer("<ge>", "", input_token_type=symbol_table),
                pynini.concat(
                  alphabet,
                  pynini.concat(
                    symbol_sets.stem_type_features(symbol_table),
                    pynini.acceptor("<nativ>", token_type=symbol_table)
                    )
                  )
                )
              )
            )
          )
        )
      )
  return pynini.concat(del_ge, symbol_sets.inflection_classes(symbol_table).closure(0, 1))

def compound_filter(symbol_table):
  '''
  Construct the compound filter
  '''

  alphabet = pynini.union(
      symbol_sets.characters(symbol_table),
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>"], input_token_type=symbol_table, output_token_type=symbol_table),
      symbol_sets.stem_types(symbol_table),
      pynini.transducer(symbol_sets.categories(symbol_table), ""),
      pynini.transducer(symbol_sets.origin_features(symbol_table), ""),
      pynini.transducer("<NoPref>", "", input_token_type=symbol_table)
      )

  return pynini.concat(
      pynini.union(
        pynini.transducer("<Initial>", "", input_token_type=symbol_table),
        pynini.acceptor("<NoHy>", token_type=symbol_table),
        pynini.acceptor("<NoDef>", token_type=symbol_table)
        ).closure(0,1),
      pynini.concat(
        pynini.union(
          pynini.concat(
            alphabet.closure(),
            pynini.transducer(pynini.string_map(["<ABK>", "<ADV>", "<CARD>", "<NE>", "<PRO>", "<V>", "<ORD>", "<OTHER>"], input_token_type=symbol_table, output_token_type=symbol_table), "")
            ),
          pynini.concat(
            pynini.transducer("", "<VADJ>", output_token_type=symbol_table),
            pynini.concat(
              pynini.union(
                alphabet,
                pynini.transducer("<kompos>", "", input_token_type=symbol_table)
                ).closure(),
              pynini.concat(
                pynini.transducer("<kompos>", "", input_token_type=symbol_table),
                pynini.concat(
                  alphabet.closure(),
                  pynini.transducer("<V>", "", input_token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.union(
              alphabet,
              pynini.transducer("<kompos>", "", input_token_type=symbol_table)
              ).closure(),
            pynini.transducer(pynini.string_map(["<ADJ>", "<NN>"], input_token_type=symbol_table, output_token_type=symbol_table), "")
            )
          ),
        pynini.concat(
          pynini.transducer("<base>", "", input_token_type=symbol_table),
          pynini.concat(
            symbol_sets.origin_features(symbol_table),
            symbol_sets.inflection_classes(symbol_table)
            )
          )
        )
      )
