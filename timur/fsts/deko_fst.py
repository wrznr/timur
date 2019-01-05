# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class DekoFst:
  '''
  Enforcement of derivation and composition constraints
  '''

  def __init__(self, syms):

    # store alphabet
    self.__syms = syms

    # TAIL
    self.__tail = self.__construct_tail()

    # origin filter
    self.__origin_filter = self.__construct_origin_filter()

    # stem_type filter
    self.__stem_type_filter = self.__construct_stem_type_filter()

    # category filter
    self.__category_filter = self.__construct_category_filter()

    # umlautung
    self.__umlautung = self.__construct_umlautung()

    suff_filter_helper = pynini.compose(
      self.__origin_filter,
      pynini.compose(
        self.__stem_type_filter,
        pynini.compose(
          self.__category_filter,
          self.__umlautung
          )
        )
      ).optimize()
    suff_phon = self.__construct_suff_phon()
    self.__suff_filter = pynini.compose(suff_filter_helper, suff_phon).optimize()

  @property
  def suff_filter(self):
    '''
    Return the complete suffix filter 
    '''
    return self.__suff_filter

  def __construct_tail(self):
    '''
    Define possible final sequences of a derivation
    '''

    # C1
    initial_stuff = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>", "<Pref_Stems>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
      ).closure()
    # C2
    intermediate_stuff = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<Suff_Stems>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
      ).closure()

    # C3
    final_stuff = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
      self.__syms.categories,
      self.__syms.stem_type_features,
      self.__syms.origin_features,
      pynini.string_map(["<NSNeut_es_e>", "<NSFem_0_n>", "<NSFem_0_en>", "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
      ).closure()

    # TAIL
    return pynini.concat(
      pynini.concat(
        initial_stuff,
        pynini.concat(
          self.__syms.base_stem_types,
          intermediate_stuff
          )
        ).closure(0,1),
      pynini.concat(
        final_stuff,
        self.__syms.inflection_classes.closure(0,1)
        )
      ).optimize()

  def __construct_origin_filter(self):
    '''
    Filter-out non-matching origin feature sequences
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
        self.__syms.stem_types,
        self.__syms.categories,
        self.__syms.stem_type_features
        ).closure()

    filtering = self.__suff_stems_filter(["<nativ>", "<frei>", "<gebunden>", "<kurz>", "<lang>", "<fremd>", "<klassisch>", "<NSNeut_es_e>", "<NSFem_0_n>", "<NSFem_0_en>", "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>", "<NGeo-$isch-Adj+>", "<NGeo-0-Name-Fem_0>", "<NGeo-0-Name-Masc_s>", "<NGeo-0-Name-Neut_s>", "<NGeo-a-Name-Fem_s>", "<NGeo-a-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-aner-Adj0-Up>", "<NGeo-anisch-Adj+>", "<NGeo-e-NMasc_n_n>", "<NGeo-e-Name-Fem_0>", "<NGeo-e-Name-Neut_s>", "<NGeo-ei-Name-Fem_0>", "<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>", "<NGeo-0-NMasc_s_0>", "<NGeo-0-Adj0-Up>", "<NGeo-erisch-Adj+>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>", "<NGeo-ien-Name-Neut_s>", "<NGeo-ier-NMasc_s_0>", "<NGeo-isch-Adj+>", "<NGeo-istan-Name-Neut_s>", "<NGeo-land-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-ner-Adj0-Up>", "<NGeo-nisch-Adj+>"])

    return pynini.concat(
        pynini.concat(
          alphabet,
          filtering
          ).closure(),
        self.__tail
        ).optimize()

  def __suff_stems_filter(self, features):
    '''
    Return a union over filters for each feature given
    '''
    filtering = pynini.Fst()
    filtering.set_input_symbols(self.__syms.alphabet)
    filtering.set_output_symbols(self.__syms.alphabet)
    suff_stems = pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet)
    for feature in features:
      to_eps = pynini.transducer(feature, "", input_token_type=self.__syms.alphabet)
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
    return filtering.optimize()

  def __construct_stem_type_filter(self):
    '''
    Filter-out non-matching stem type sequences
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
        self.__syms.stem_types,
        self.__syms.categories,
        ).closure()

    filtering = self.__suff_stems_filter(["<deriv>", "<kompos>"])

    return pynini.concat(
        pynini.concat(
          alphabet,
          filtering
          ).closure(),
        self.__tail
        ).optimize()

  def __construct_category_filter(self):
    '''
    Filter-out non-matching category sequences
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
        self.__syms.stem_types,
        self.__syms.categories,
        ).closure()

    filtering = self.__suff_stems_filter(["<ABK>", "<ADJ>", "<ADV>", "<CARD>", "<DIGCARD>", "<NE>", "<NN>", "<PRO>", "<V>", "<ORD>"])

    return pynini.concat(
        pynini.concat(
          alphabet,
          filtering
          ).closure(),
        self.__tail
        ).optimize()

  def __construct_umlautung(self):
    '''
    Map "a", "o" and "u" onto "ä", "ö" and "ü", corresp., if the umlaut marker "<UL>" is present.
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
        self.__syms.stem_types,
        self.__syms.categories,
        ).closure()

    return pynini.concat(
        pynini.concat(
          alphabet,
          pynini.concat(
            self.__syms.consonants,
            pynini.concat(
              pynini.union(
                pynini.union(
                  pynini.transducer("a", "ä", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
                  pynini.transducer("o", "ö", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
                  pynini.transducer("u", "ü", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
                  ),
                pynini.concat(
                  pynini.transducer("a", "ä", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
                  pynini.union(
                    pynini.transducer("a", "", input_token_type=self.__syms.alphabet),
                    pynini.acceptor("u", token_type=self.__syms.alphabet)
                    )
                  )
                ),
              pynini.concat(
                self.__syms.consonants.closure(),
                pynini.concat(
                  pynini.concat(
                    pynini.acceptor("e", token_type=self.__syms.alphabet),
                    pynini.string_map(["l", "r"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
                    ).closure(0, 1),
                  pynini.concat(
                    pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet),
                    pynini.transducer("<UL>", "", input_token_type=self.__syms.alphabet)
                    )
                  )
                )
              )
            ).closure(0, 1)
          ),
        self.__tail
        ).optimize()

  def __construct_suff_phon(self):
    '''
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>", "<NN>", "<ADJ>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
        self.__syms.stem_types,
        ).closure()

    return pynini.concat(
        pynini.cdrewrite(
          pynini.transducer("i", "", input_token_type=self.__syms.alphabet),
          pynini.concat(
            pynini.union(
              pynini.acceptor("i", token_type=self.__syms.alphabet),
              pynini.concat(
                self.__syms.consonants,
                pynini.acceptor("y", token_type=self.__syms.alphabet)
                )
              ),
            pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet)
            ),
          "",
          alphabet
          ),
        self.__tail
        ).optimize()

def prefix_filter(symbol_table):
  '''
  Construct the (complete) prefix filter
  '''

  alphabet = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=symbol_table, output_token_type=symbol_table),
      self.__syms.stem_types,
      self.__syms.categories,
      ).closure()

  # delete <ge> at certain suffixes like 'ver'
  del_ge = pynini.concat(
      pynini.transducer("<no-ge>", "", input_token_type=symbol_table),
      pynini.concat(
        pynini.acceptor("<Pref_Stems>", token_type=symbol_table),
        pynini.concat(
          pynini.union(
            self.__syms.characters,
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
                    self.__syms.stem_type_features,
                    pynini.acceptor("<nativ>", token_type=symbol_table)
                    )
                  )
                )
              )
            )
          )
        )
      )
  # match origin of prefix and stem
  prefix_origin_filter = pynini.concat(
      pynini.acceptor("<Pref_Stems>", token_type=symbol_table),
      pynini.concat(
        pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>"], input_token_type=symbol_table, output_token_type=symbol_table)
          ).closure(),
        pynini.union(
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<ADJ>", token_type=symbol_table),
                pynini.acceptor("<nativ>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<ADJ>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.acceptor("<nativ>", token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<ABK>", token_type=symbol_table),
                pynini.acceptor("<nativ>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<ABK>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.acceptor("<nativ>", token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<NN>", token_type=symbol_table),
                pynini.acceptor("<nativ>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<NN>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.acceptor("<nativ>", token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<NN>", token_type=symbol_table),
                pynini.acceptor("<fremd>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<NN>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.acceptor("<fremd>", token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<NE>", token_type=symbol_table),
                pynini.acceptor("<nativ>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<NE>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.acceptor("<nativ>", token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<NE>", token_type=symbol_table),
                pynini.acceptor("<fremd>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<NE>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.acceptor("<fremd>", token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<ADJ>", token_type=symbol_table),
                pynini.acceptor("<fremd>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<ADJ>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.acceptor("<fremd>", token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<V>", token_type=symbol_table),
                pynini.acceptor("<nativ>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<V>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.acceptor("<nativ>", token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<V>", token_type=symbol_table),
                pynini.acceptor("<nativ>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<V>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  self.__syms.ns_features
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<ADJ>", token_type=symbol_table),
                pynini.acceptor("<klassisch>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<ADJ>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"], input_token_type=symbol_table, output_token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<NN>", token_type=symbol_table),
                pynini.acceptor("<klassisch>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<NN>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"], input_token_type=symbol_table, output_token_type=symbol_table)
                  )
                )
              )
            ),
          pynini.concat(
            pynini.transducer(
              pynini.concat(
                pynini.acceptor("<V>", token_type=symbol_table),
                pynini.acceptor("<klassisch>", token_type=symbol_table)
                ),
              ""
              ),
            pynini.concat(
              alphabet,
              pynini.concat(
                pynini.acceptor("<V>", token_type=symbol_table),
                pynini.concat(
                  self.__syms.stem_type_features,
                  pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"], input_token_type=symbol_table, output_token_type=symbol_table)
                  )
                )
              )
            )
          )
        )
      )

  return pynini.concat(pynini.union(del_ge, prefix_origin_filter), self.__syms.inflection_classes.closure(0, 1))

def compound_filter(symbol_table):
  '''
  Construct the compound filter
  '''

  alphabet = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>"], input_token_type=symbol_table, output_token_type=symbol_table),
      self.__syms.stem_types,
      pynini.transducer(self.__syms.categories, ""),
      pynini.transducer(self.__syms.origin_features, ""),
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
            self.__syms.origin_features,
            self.__syms.inflection_classes
            )
          )
        )
      )

def insert_ge(symbol_table):
  '''
  Inserts the prefix "ge" controlled by the symbol "<ge>"
  '''

  alphabet = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^imp>", "<^zz>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"], input_token_type=symbol_table, output_token_type=symbol_table),
      self.__syms.stem_types,
      )

  c2 = pynini.union(
      alphabet,
      self.__syms.stem_types
      ).closure()
  
  # From deko.fst:
  # replace <ge> with "ge" if followed by perfect participle marker
  # or ge-nominalisation otherwise delete <ge>
  # in complex lexicon entries as for "haushalten" <ge> is not followed
  # by <Base_Stems>
  return pynini.union(
      c2,
      pynini.concat(
        c2,
        pynini.concat(
          pynini.transducer("<ge>", "", input_token_type=symbol_table),
          pynini.concat(
            pynini.acceptor("<Base_Stems>", token_type=symbol_table).closure(0, 1),
            pynini.concat(
              pynini.transducer("", "g e", output_token_type=symbol_table),
              pynini.concat(
                alphabet.closure(),
                pynini.concat(
                  pynini.transducer("<^pp>", "", input_token_type=symbol_table),
                  alphabet.closure()
                  )
                )
              )
            )
          )
        ),
      pynini.concat(
        c2,
        pynini.concat(
          pynini.transducer("<ge>", "", input_token_type=symbol_table),
          pynini.concat(
            pynini.acceptor("<Deriv_Stems>", token_type=symbol_table).closure(0, 1),
            pynini.concat(
              pynini.transducer("", "g e", output_token_type=symbol_table),
              pynini.concat(
                alphabet.closure(),
                pynini.concat(
                  pynini.transducer("<Suff_Stems> <Ge-Nom>", "e", input_token_type=symbol_table, output_token_type=symbol_table),
                  alphabet.closure()
                  )
                )
              )
            )
          )
        ),
      pynini.concat(
        c2,
        pynini.concat(
          pynini.transducer("<ge>", "", input_token_type=symbol_table),
          pynini.concat(
            pynini.acceptor("<Base_Stems>", token_type=symbol_table).closure(0, 1),
            alphabet.closure()
            )
          )
        ),
      pynini.concat(
        c2,
        pynini.concat(
          pynini.acceptor("<Base_Stems>", token_type=symbol_table).closure(0, 1),
          pynini.concat(
            alphabet.closure(),
            pynini.concat(
              pynini.transducer("<^pp>", "", input_token_type=symbol_table),
              alphabet.closure()
              )
            )
          )
        )
      )

def insert_zu(symbol_table):
  '''
  Inserts "zu" into infinitives with separable prefixes
  '''

  alphabet = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^imp>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"], input_token_type=symbol_table, output_token_type=symbol_table),
      self.__syms.stem_types,
      )

  c2 = pynini.union(
      alphabet,
      self.__syms.stem_types
      ).closure()
  
  # From deko.fst:
  # insert "zu" after verbal prefixes if followed by infinitive marker
  return pynini.union(
      c2,
      pynini.concat(
        pynini.acceptor("<Base_Stems>", token_type=symbol_table),
        pynini.concat(
          alphabet.closure(),
          pynini.concat(
            pynini.transducer("<^zz>", "", input_token_type=symbol_table),
            alphabet.closure()
            )
          )
        ),
      pynini.concat(
        c2,
        pynini.concat(
          pynini.acceptor("<Pref_Stems>", token_type=symbol_table),
          pynini.concat(
            alphabet.closure(),
            pynini.concat(
              pynini.acceptor("<Base_Stems>", token_type=symbol_table),
              pynini.concat(
                pynini.transducer("", "z u", output_token_type=symbol_table),
                pynini.concat(
                  alphabet.closure(),
                  pynini.concat(
                    pynini.transducer("<^zz>", "", input_token_type=symbol_table),
                    alphabet.closure()
                    )
                  )
                )
              )
            )
          )
        )
      )

def imperative_filter(symbol_table):
  '''
  Imperatives have no separable prefixes
  '''

  alphabet = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"], input_token_type=symbol_table, output_token_type=symbol_table),
      self.__syms.stem_types
      )

  c2 = pynini.union(
      alphabet,
      pynini.transducer(self.__syms.stem_types, "<CB>", input_token_type=symbol_table, output_token_type=symbol_table)
      ).closure()

  return pynini.union(
      c2,
      pynini.concat(
        pynini.transducer("<Base_Stems>", "<CB>", input_token_type=symbol_table, output_token_type=symbol_table),
        pynini.concat(
          alphabet.closure(),
          pynini.concat(
            pynini.transducer("<^imp>", "", input_token_type=symbol_table),
            alphabet.closure()
            )
          )
        )
      )

def infix_filter(symbol_table):
  '''
  Combination of the different infix filter
  '''
  return pynini.compose(
      insert_ge(symbol_table),
      pynini.compose(
        insert_zu(symbol_table),
        imperative_filter(symbol_table)
        )
      )

def uplow(symbol_table):
  '''
  Upper/Lower case markers
  '''

  alphabet = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoDef>", "<FB>", "<UL>", "<SS>", "<DEL-S>",  "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<^imp>", "<ge>", "<^zz>"], input_token_type=symbol_table, output_token_type=symbol_table)
      )
  
  s = pynini.concat(
      alphabet,
      pynini.union(
        alphabet,
        pynini.acceptor("<CB>", token_type=symbol_table)
        ).closure()
      )

  s2 = pynini.concat(
      pynini.union(
        pynini.concat(
          pynini.transducer("<CB>", "", input_token_type=symbol_table),
          self.__syms.characters_upper
          ),
        pynini.concat(
          pynini.transducer("<CB>", "", input_token_type=symbol_table).closure(0, 1),
          self.__syms.characters_lower
          )
        ),
      s
      )

  return pynini.union(
      pynini.concat(
          pynini.transducer("<^UC>", "", input_token_type=symbol_table),
          pynini.concat(
            pynini.string_map(["<NoDef>", "<NoHy>"], input_token_type=symbol_table, output_token_type=symbol_table).closure(0, 1),
            pynini.concat(
              pynini.transducer("", "<^UC>", output_token_type=symbol_table),
              pynini.concat(
                s2,
                pynini.transducer("<Low#>", "", input_token_type=symbol_table)
                )
              )
            )
        ),
      pynini.concat(
        pynini.acceptor("<NoHy>", token_type=symbol_table).closure(0, 1),
        pynini.union(
          pynini.concat(
            pynini.transducer("<CB>", "", input_token_type=symbol_table),
            pynini.concat(
              s,
              pynini.transducer("<Fix#>", "", input_token_type=symbol_table)
              )
            ),
          pynini.concat(
            pynini.transducer(pynini.string_map(["<CB>", "<epsilon>"], input_token_type=symbol_table, output_token_type=symbol_table), "<^UC>", output_token_type=symbol_table),
            pynini.concat(
              s,
              pynini.transducer("<Up#>", "", input_token_type=symbol_table)
              )
            ),
          pynini.concat(
            pynini.transducer(pynini.string_map(["<CB>", "<epsilon>"], input_token_type=symbol_table, output_token_type=symbol_table), "<CB>", output_token_type=symbol_table),
            pynini.concat(
              s,
              pynini.transducer("<Low#>", "", input_token_type=symbol_table)
              )
            )
          )
        )
      )
