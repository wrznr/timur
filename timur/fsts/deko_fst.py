# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class DekoFst:
  '''
  Enforcement of derivation and composition constraints
  '''

  def __init__(self, syms):

    #
    # store alphabet
    self.__syms = syms

    #
    # suffix filter

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

    # suffix phonology
    self.__suff_phon = self.__construct_suff_phon()

    # putting it all together
    self.__suff_filter = (self.__origin_filter * self.__stem_type_filter * self.__category_filter * self.__umlautung * self.__suff_phon).optimize()

    #
    # prefix filter

    # prefix filter helper
    self.__prefix_filter_helper = self.__construct_prefix_filter_helper()

    # del ge
    self.__del_ge = self.__construct_del_ge()

    # prefix origin filter
    self.__prefix_origin_filter = self.__construct_prefix_origin_filter()

    # repeatable prefixation
    self.__rep_pref = self.__construct_rep_pref()

    self.__pref_filter = pynini.concat(pynini.union(self.__del_ge, self.__prefix_origin_filter, self.__rep_pref), self.__syms.inflection_classes.closure(0, 1)).optimize()

    #
    # compound filter
    self.__compound_filter = self.__construct_compound_filter()

    #
    # infix filter

    # insert ge
    self.__insert_ge = self.__construct_insert_ge()

    # insert zu
    self.__insert_zu = self.__construct_insert_zu()

    # imperative filter
    self.__imperative_filter = self.__construct_imperative_filter()

    self.__infix_filter = (self.__insert_ge * self.__insert_zu * self.__imperative_filter).optimize()

    #
    # uplow
    self.__uplow = self.__construct_uplow()

  @property
  def suff_filter(self):
    '''
    Return the complete suffix filter 
    '''
    return self.__suff_filter

  @property
  def pref_filter(self):
    '''
    Return the complete prefix filter 
    '''
    return self.__pref_filter

  @property
  def compound_filter(self):
    '''
    Return the complete compound filter 
    '''
    return self.__compound_filter

  @property
  def infix_filter(self):
    '''
    Return the complete infix filter 
    '''
    return self.__infix_filter

  @property
  def uplow(self):
    '''
    Return the upper/lower case realizer
    '''
    return self.__uplow

  def __construct_tail(self):
    '''
    Define possible final sequences of a derivation
    '''

    # C1
    initial_stuff = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>", "<Pref_Stems>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
      ).closure()
    # C2
    intermediate_stuff = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<Suff_Stems>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
      ).closure()

    # C3
    final_stuff = pynini.union(
      self.__syms.characters,
      pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
      self.__syms.categories,
      self.__syms.stem_type_features,
      self.__syms.origin_features,
      pynini.string_map(["<NSNeut_es_e>", "<NSFem_0_n>", "<NSFem_0_en>", "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
      ).closure()

    # TAIL
    return pynini.concat(
      pynini.concat(
        initial_stuff,
        self.__syms.base_stem_types,
        intermediate_stuff
        ).closure(0,1),
      final_stuff,
      self.__syms.inflection_classes.closure(0,1)
      ).optimize()

  def __construct_origin_filter(self):
    '''
    Filter-out non-matching origin feature sequences
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
        self.__syms.stem_types,
        self.__syms.categories,
        self.__syms.stem_type_features
        ).closure().optimize()

    filtering = self.__suff_stems_filter(["<nativ>", "<prefnativ>", "<frei>", "<gebunden>", "<kurz>", "<lang>", "<fremd>", "<klassisch>", "<NSNeut_es_e>", "<NSFem_0_n>", "<NSFem_0_en>", "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>", "<NGeo-$er-NMasc_s_0>", "<NGeo-$er-Adj0-Up>", "<NGeo-$isch-Adj+>", "<NGeo-0-Name-Fem_0>", "<NGeo-0-Name-Masc_s>", "<NGeo-0-Name-Neut_s>", "<NGeo-a-Name-Fem_s>", "<NGeo-a-Name-Neut_s>", "<NGeo-aner-NMasc_s_0>", "<NGeo-aner-Adj0-Up>", "<NGeo-anisch-Adj+>", "<NGeo-e-NMasc_n_n>", "<NGeo-e-Name-Fem_0>", "<NGeo-e-Name-Neut_s>", "<NGeo-ei-Name-Fem_0>", "<NGeo-en-Name-Neut_s>", "<NGeo-er-NMasc_s_0>", "<NGeo-er-Adj0-Up>", "<NGeo-0-NMasc_s_0>", "<NGeo-0-Adj0-Up>", "<NGeo-erisch-Adj+>", "<NGeo-ese-NMasc_n_n>", "<NGeo-esisch-Adj+>", "<NGeo-ianer-NMasc_s_0>", "<NGeo-ianisch-Adj+>", "<NGeo-ien-Name-Neut_s>", "<NGeo-ier-NMasc_s_0>", "<NGeo-isch-Adj+>", "<NGeo-istan-Name-Neut_s>", "<NGeo-land-Name-Neut_s>", "<NGeo-ner-NMasc_s_0>", "<NGeo-ner-Adj0-Up>", "<NGeo-nisch-Adj+>"])

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
            to_eps,
            suff_stems,
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
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
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
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
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
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
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
                    pynini.string_map(["l", "r"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
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
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>", "<NN>", "<ADJ>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
        self.__syms.stem_types,
        ).closure()

    Tau = pynini.transducer("i", "", input_token_type=self.__syms.alphabet)
    Lambda = pynini.concat(
        pynini.union(
          pynini.acceptor("i", token_type=self.__syms.alphabet),
          pynini.concat(
            self.__syms.consonants.project(),
            pynini.acceptor("y", token_type=self.__syms.alphabet)
            )
          ),
        pynini.acceptor("<Suff_Stems>", token_type=self.__syms.alphabet)
        )

    return pynini.concat(
        pynini.cdrewrite(
          Tau,
          Lambda,
          "",
          alphabet.project()
          ),
        self.__tail
        ).optimize()

  def __construct_prefix_filter_helper(self):
    '''
    Alphabet for the prefix filter
    '''

    return pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
        self.__syms.stem_types,
        self.__syms.categories,
        ).closure().optimize()

  def __construct_rep_pref(self):
    '''
    Replace the marker of manually prefixed stems
    '''
    return pynini.cdrewrite(
        pynini.transducer("<prefnativ>", "<nativ>"),
        "",
        "",
        self.__prefix_filter_helper
        ).optimize()

  def __construct_del_ge(self):
    '''
    Case-dependent deletion of the ge marker
    '''

    # delete <ge> at certain suffixes like 'ver'
    return pynini.concat(
        pynini.transducer("<no-ge>", "", input_token_type=self.__syms.alphabet),
        pynini.concat(
          pynini.acceptor("<Pref_Stems>", token_type=self.__syms.alphabet),
          pynini.concat(
            pynini.union(
              self.__syms.characters,
              pynini.string_map(["<n>", "<e>", "<d>", "<~n>"]).project()
              ).closure(),
            pynini.concat(
              pynini.transducer("<V> <nativ>", "", input_token_type=self.__syms.alphabet),
              pynini.acceptor("<NoDef>", token_type=self.__syms.alphabet).closure(0, 1),
              pynini.transducer("<ge>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              self.__syms.stem_type_features,
              pynini.acceptor("<nativ>", token_type=self.__syms.alphabet)
              )
            )
          )
        ).optimize()

  def __construct_prefix_origin_filter(self):
    '''
    Match origin of prefix and stem
    '''

    return pynini.concat(
        pynini.acceptor("<Pref_Stems>", token_type=self.__syms.alphabet),
        pynini.concat(
          pynini.union(
            self.__syms.characters,
            pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
            ).closure(),
          pynini.union(
            pynini.concat(
              pynini.transducer("<ADJ> <nativ>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<ADJ>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.acceptor("<nativ>", token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer("<ABK> <nativ>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<ABK>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.acceptor("<nativ>", token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer("<NN> <nativ>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<NN>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.acceptor("<nativ>", token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer("<NN> <fremd>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<NN>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.acceptor("<fremd>", token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer("<NE> <nativ>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<NE>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.acceptor("<nativ>", token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer("<NE> <fremd>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<NE>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.acceptor("<fremd>", token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer("<ADJ> <fremd>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<ADJ>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.acceptor("<fremd>", token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer("<V> <nativ>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<V>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.acceptor("<nativ>", token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer("<V> <nativ>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<V>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              self.__syms.ns_features
              ),
            pynini.concat(
              pynini.transducer("<ADJ> <klassisch>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<ADJ>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
              ),
            pynini.concat(
              pynini.transducer("<NN> <klassisch>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<NN>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
              ),
            pynini.concat(
              pynini.transducer("<V> <klassisch>", "", input_token_type=self.__syms.alphabet),
              self.__prefix_filter_helper,
              pynini.acceptor("<V>", token_type=self.__syms.alphabet),
              self.__syms.stem_type_features,
              pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
              )
            )
          )
        ).optimize()

  def __construct_compound_filter(self):
    '''
    Construct the compound filter
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
        self.__syms.stem_types,
        pynini.transducer(self.__syms.categories, ""),
        pynini.transducer(self.__syms.origin_features, ""),
        pynini.transducer("<NoPref>", "", input_token_type=self.__syms.alphabet)
        )

    return pynini.concat(
        pynini.union(
          pynini.transducer("<Initial>", "", input_token_type=self.__syms.alphabet),
          pynini.acceptor("<NoHy>", token_type=self.__syms.alphabet),
          pynini.acceptor("<NoDef>", token_type=self.__syms.alphabet)
          ).closure(0,1),
        pynini.concat(
          pynini.union(
            pynini.concat(
              alphabet.closure(),
              pynini.transducer(pynini.string_map(["<ABK>", "<ADV>", "<CARD>", "<NE>", "<PRO>", "<V>", "<ORD>", "<OTHER>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(), "")
              ),
            pynini.concat(
              pynini.transducer("", "<VADJ>", output_token_type=self.__syms.alphabet),
              pynini.union(
                alphabet,
                pynini.transducer("<kompos>", "", input_token_type=self.__syms.alphabet)
                ).closure(),
              pynini.transducer("<kompos>", "", input_token_type=self.__syms.alphabet),
              alphabet.closure(),
              pynini.transducer("<V>", "", input_token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.union(
                alphabet,
                pynini.transducer("<kompos>", "", input_token_type=self.__syms.alphabet)
                ).closure(),
              pynini.transducer(pynini.string_map(["<ADJ>", "<NN>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(), "")
              )
            ),
          pynini.concat(
            pynini.transducer("<base>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer(self.__syms.origin_features, ""),
            self.__syms.inflection_classes
            )
          )
        ).optimize()

  def __construct_insert_ge(self):
    '''
    Inserts the prefix "ge" controlled by the symbol "<ge>"
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^imp>", "<^zz>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        ).optimize()

    c2 = pynini.union(
        alphabet,
        self.__syms.stem_types
        ).closure().optimize()
    
    # From deko.fst:
    # replace <ge> with "ge" if followed by perfect participle marker
    # or ge-nominalisation otherwise delete <ge>
    # in complex lexicon entries as for "haushalten" <ge> is not followed
    # by <Base_Stems>
    return pynini.union(
        c2,
        pynini.concat(
          c2,
          pynini.transducer("<ge>", "", input_token_type=self.__syms.alphabet),
          pynini.acceptor("<Base_Stems>", token_type=self.__syms.alphabet).closure(0, 1),
          pynini.transducer("", "g e", output_token_type=self.__syms.alphabet),
          alphabet.closure(),
          pynini.transducer("<^pp>", "", input_token_type=self.__syms.alphabet),
          alphabet.closure()
          ),
        pynini.concat(
          c2,
          pynini.acceptor("<Deriv_Stems>", token_type=self.__syms.alphabet).closure(0, 1),
          alphabet.closure(),
          pynini.transducer("<Ge>", "", input_token_type=self.__syms.alphabet),
          alphabet.closure(),
          pynini.transducer("<Suff_Stems> <Ge-Nom>", "e", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          alphabet.closure()
          ),
        pynini.concat(
          c2,
          pynini.transducer("<ge>", "", input_token_type=self.__syms.alphabet),
          pynini.acceptor("<Base_Stems>", token_type=self.__syms.alphabet).closure(0, 1),
          alphabet.closure()
          ),
        pynini.concat(
          c2,
          pynini.acceptor("<Base_Stems>", token_type=self.__syms.alphabet).closure(0, 1),
          alphabet.closure(),
          pynini.transducer("<^pp>", "", input_token_type=self.__syms.alphabet),
          alphabet.closure()
          )
        ).optimize()

  def __construct_insert_zu(self):
    '''
    Inserts "zu" into infinitives with separable prefixes
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^imp>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        ).optimize()

    c2 = pynini.union(
        alphabet,
        self.__syms.stem_types
        ).closure().optimize()
    
    # From deko.fst:
    # insert "zu" after verbal prefixes if followed by infinitive marker
    return pynini.union(
        c2,
        #pynini.concat(
        #  pynini.acceptor("<Base_Stems>", token_type=self.__syms.alphabet),
        #  alphabet.closure(),
        #  pynini.transducer("<^zz>", "", input_token_type=self.__syms.alphabet),
        #  alphabet.closure()
        #  ),
        pynini.concat(
          c2,
          pynini.acceptor("<Pref_Stems>", token_type=self.__syms.alphabet),
          alphabet.closure(),
          pynini.acceptor("<Base_Stems>", token_type=self.__syms.alphabet),
          pynini.transducer("", "z u", output_token_type=self.__syms.alphabet),
          alphabet.closure(),
          pynini.transducer("<^zz>", "", input_token_type=self.__syms.alphabet),
          alphabet.closure()
          )
        ).optimize()

  def __construct_imperative_filter(self):
    '''
    Imperatives have no separable prefixes
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        ).optimize()

    c2 = pynini.union(
        alphabet,
        pynini.transducer(self.__syms.stem_types, "<CB>", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
        ).closure().optimize()

    return pynini.union(
        c2,
        pynini.concat(
          pynini.transducer("<Base_Stems>", "<CB>", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          alphabet.closure(),
          pynini.transducer("<^imp>", "", input_token_type=self.__syms.alphabet),
          alphabet.closure()
          )
        ).optimize()

  def __construct_uplow(self):
    '''
    Upper/Lower case markers
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoDef>", "<FB>", "<UL>", "<SS>", "<DEL-S>",  "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<^imp>", "<ge>", "<^zz>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        ).optimize()
    
    s = pynini.concat(
        alphabet,
        pynini.union(
          alphabet,
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet)
          ).closure()
        ).optimize()

    s2 = pynini.concat(
        pynini.union(
          pynini.concat(
            pynini.transducer("<CB>", "", input_token_type=self.__syms.alphabet),
            self.__syms.characters_upper
            ),
          pynini.concat(
            pynini.transducer("<CB>", "", input_token_type=self.__syms.alphabet).closure(0, 1),
            self.__syms.characters_lower
            )
          ),
        s
        ).optimize()

    return pynini.union(
        pynini.concat(
            pynini.transducer("<^UC>", "", input_token_type=self.__syms.alphabet),
            pynini.string_map(["<NoDef>", "<NoHy>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project().closure(0, 1),
            pynini.transducer("", "<^UC>", output_token_type=self.__syms.alphabet),
            s2,
            pynini.transducer("<Low#>", "", input_token_type=self.__syms.alphabet)
          ),
        pynini.concat(
          pynini.acceptor("<NoHy>", token_type=self.__syms.alphabet).closure(0, 1),
          pynini.union(
            pynini.concat(
              pynini.transducer("<CB>", "", input_token_type=self.__syms.alphabet),
              s,
              pynini.transducer("<Fix#>", "", input_token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer(pynini.string_map(["<CB>", "<epsilon>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(), "<^UC>", output_token_type=self.__syms.alphabet),
              s,
              pynini.transducer("<Up#>", "", input_token_type=self.__syms.alphabet)
              ),
            pynini.concat(
              pynini.transducer(pynini.string_map(["<CB>", "<epsilon>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(), "<CB>", output_token_type=self.__syms.alphabet),
              s,
              pynini.transducer("<Low#>", "", input_token_type=self.__syms.alphabet)
              )
            )
          )
        ).optimize()
