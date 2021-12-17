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
    self.__suff_filter = (self.__origin_filter @ self.__stem_type_filter @ self.__category_filter @ self.__umlautung @ self.__suff_phon).optimize()

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

    self.__infix_filter = (self.__insert_ge @ self.__insert_zu @ self.__imperative_filter).optimize()

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
    with pynini.default_token_type(self.__syms.alphabet):

      # C1
      initial_stuff = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>", "<Pref_Stems>"]).project("input")
        ).closure()
      # C2
      intermediate_stuff = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<Suff_Stems>"]).project("input")
        ).closure()

      # C3
      final_stuff = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>"]).project("input"),
        self.__syms.categories,
        self.__syms.stem_type_features,
        self.__syms.origin_features,
        pynini.string_map(["<NSNeut_es_e>", "<NSFem_0_n>", "<NSFem_0_en>", "<NSMasc_es_e>", "<NSMasc_es_$e>", "<NSMasc-s/$sse>"]).project("input")
        ).closure()

      # TAIL
      tail1 = initial_stuff + self.__syms.base_stem_types + intermediate_stuff
      return pynini.concat(tail1.closure(0,1) + final_stuff, self.__syms.inflection_classes.closure(0,1)).optimize()

  def __construct_origin_filter(self):
    '''
    Filter-out non-matching origin feature sequences
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"]).project("input"),
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
    with pynini.default_token_type(self.__syms.alphabet):
      filtering = pynini.Fst()
      filtering.set_input_symbols(self.__syms.alphabet)
      filtering.set_output_symbols(self.__syms.alphabet)
      suff_stems = pynini.accep("<Suff_Stems>")
      for feature in features:
        to_eps = pynini.cross(feature, "")
        filtering = pynini.union(
            filtering,
            to_eps + suff_stems + to_eps
            )
      return filtering.optimize()

  def __construct_stem_type_filter(self):
    '''
    Filter-out non-matching stem type sequences
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"]).project("input"),
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
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"]).project("input"),
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
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"]).project("input"),
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
                    pynini.cross("a", "ä"),
                    pynini.cross("o", "ö"),
                    pynini.cross("u", "ü")
                    ),
                  pynini.concat(
                    pynini.cross("a", "ä"),
                    pynini.union(
                      pynini.cross("a", ""),
                      pynini.accep("u")
                      )
                    )
                  ),
                pynini.concat(
                  self.__syms.consonants.closure(),
                  pynini.concat(
                    pynini.concat(
                      pynini.accep("e"),
                      pynini.string_map(["l", "r"]).project("input")
                      ).closure(0, 1),
                    pynini.concat(
                      pynini.accep("<Suff_Stems>"),
                      pynini.cross("<UL>", "")
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
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>", "<NN>", "<ADJ>"]).project("input"),
          self.__syms.stem_types,
          ).closure()

      Tau = pynini.cross("i", "")
      Lambda = pynini.concat(
          pynini.union(
            pynini.accep("i"),
            pynini.concat(
              self.__syms.consonants.project("input"),
              pynini.accep("y")
              )
            ),
          pynini.accep("<Suff_Stems>")
          )

      return pynini.concat(
          pynini.cdrewrite(
            Tau,
            Lambda,
            "",
            alphabet.project("input")
            ),
          self.__tail
          ).optimize()

  def __construct_prefix_filter_helper(self):
    '''
    Alphabet for the prefix filter
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      return pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>", "<no-ge>", "<Initial>", "<NoHy>", "<NoPref>", "<NoDef>"]).project("input"),
          self.__syms.stem_types,
          self.__syms.categories,
          ).closure().optimize()

  def __construct_rep_pref(self):
    '''
    Replace the marker of manually prefixed stems
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      return pynini.cdrewrite(
          pynini.cross("<prefnativ>", "<nativ>"),
          "",
          "",
          self.__prefix_filter_helper
          ).optimize()

  def __construct_del_ge(self):
    '''
    Case-dependent deletion of the ge marker
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      # delete <ge> at certain prefixes like 'ver'
      return pynini.concat(
          pynini.cross("<no-ge>", ""),
          pynini.concat(
            pynini.accep("<Pref_Stems>"),
            pynini.concat(
              pynini.union(
                self.__syms.characters,
                pynini.string_map(["<n>", "<e>", "<d>", "<~n>"]).project("input")
                ).closure(),
              pynini.cross("<V> <nativ>", "") + pynini.accep("<NoDef>").closure(0, 1) + pynini.cross("<ge>", "") + self.__prefix_filter_helper + self.__syms.stem_type_features + pynini.accep("<nativ>")
              )
            )
          ).optimize()

  def __construct_prefix_origin_filter(self):
    '''
    Match origin of prefix and stem
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      return pynini.concat(
          pynini.accep("<Pref_Stems>"),
          pynini.concat(
            pynini.union(
              self.__syms.characters,
              pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>"]).project("input")
              ).closure(),
            pynini.union(
              pynini.cross("<ADJ> <nativ>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<ADJ>")
              + self.__syms.stem_type_features
              + pynini.accep("<nativ>")
              ,
              pynini.cross("<ABK> <nativ>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<ABK>")
              + self.__syms.stem_type_features
              + pynini.accep("<nativ>")
              ,
              pynini.cross("<NN> <nativ>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<NN>")
              + self.__syms.stem_type_features
              + pynini.accep("<nativ>")
              ,
              pynini.cross("<NN> <fremd>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<NN>")
              + self.__syms.stem_type_features
              + pynini.accep("<fremd>")
              ,
              pynini.cross("<NE> <nativ>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<NE>")
              + self.__syms.stem_type_features
              + pynini.accep("<nativ>")
              ,
              pynini.cross("<NE> <fremd>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<NE>")
              + self.__syms.stem_type_features
              + pynini.accep("<fremd>")
              ,
              pynini.cross("<ADJ> <fremd>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<ADJ>")
              + self.__syms.stem_type_features
              + pynini.accep("<fremd>")
              ,
              pynini.cross("<V> <nativ>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<V>")
              + self.__syms.stem_type_features
              + pynini.accep("<nativ>")
              ,
              pynini.cross("<V> <nativ>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<V>")
              + self.__syms.stem_type_features
              + self.__syms.ns_features
              ,
              pynini.cross("<ADJ> <klassisch>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<ADJ>")
              + self.__syms.stem_type_features
              + pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"]).project("input")
              ,
              pynini.cross("<NN> <klassisch>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<NN>")
              + self.__syms.stem_type_features
              + pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"]).project("input")
              ,
              pynini.cross("<V> <klassisch>", "")
              + self.__prefix_filter_helper
              + pynini.accep("<V>")
              + self.__syms.stem_type_features
              + pynini.string_map(["<frei>", "<gebunden>", "<kurz>", "<lang>"]).project("input")
              )
            )
          ).optimize()

  def __construct_compound_filter(self):
    '''
    Construct the compound filter
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<SS>", "<FB>", "<ge>", "<Ge>"]).project("input"),
          self.__syms.stem_types,
          pynini.cross(self.__syms.categories, ""),
          pynini.cross(self.__syms.origin_features, ""),
          pynini.cross("<NoPref>", "")
          )

      return pynini.concat(
          pynini.union(
            pynini.cross("<Initial>", ""),
            pynini.accep("<NoHy>"),
            pynini.accep("<NoDef>")
            ).closure(0,1),
          pynini.concat(
            pynini.union(
              pynini.concat(
                alphabet.closure(),
                pynini.cross(pynini.string_map(["<ABK>", "<ADV>", "<CARD>", "<NE>", "<PRO>", "<V>", "<ORD>", "<OTHER>"]).project("input"), "")
                ),
              pynini.concat(
                pynini.cross("", "<VADJ>"),
                pynini.concat(
                  pynini.union(
                    alphabet,
                    pynini.cross("<kompos>", "")
                    ).closure(),
                  pynini.concat(
                    pynini.cross("<kompos>", ""),
                    pynini.concat(
                      alphabet.closure(),
                      pynini.cross("<V>", "")
                      )
                    )
                  )
                ),
              pynini.concat(
                pynini.union(
                  alphabet,
                  pynini.cross("<kompos>", "")
                  ).closure(),
                pynini.cross(pynini.string_map(["<ADJ>", "<NN>"]).project("input"), "")
                )
              ),
            pynini.concat(
              pynini.cross("<base>", ""),
              pynini.concat(
                pynini.cross(self.__syms.origin_features, ""),
                self.__syms.inflection_classes
                )
              )
            )
          ).optimize()

  def __construct_insert_ge(self):
    '''
    Inserts the prefix "ge" controlled by the symbol "<ge>"
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^imp>", "<^zz>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"]).project("input")
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
          c2
          ,
          c2 + pynini.cross("<ge>", "")
          + pynini.accep("<Base_Stems>").closure(0, 1)
          + pynini.cross("", "g e") + alphabet.closure()
          + pynini.cross("<^pp>", "") + alphabet.closure()
          ,
          c2 + pynini.cross("<ge>", "")
          + pynini.accep("<Base_Stems>").closure(0, 1)
          + alphabet.closure()
          ,
          c2
          + pynini.accep("<Base_Stems>").closure(0, 1)
          + alphabet.closure()
          + pynini.cross("<^pp>", "") + alphabet.closure()
          ,
          c2
          + pynini.accep("<Deriv_Stems>").closure(0, 1)
          + alphabet.closure()
          + pynini.cross("<Ge>", "")
          + alphabet.closure()
          + pynini.cross("<Suff_Stems> <Ge-Nom>", "e")
          + alphabet.closure()
          ).optimize()

  def __construct_insert_zu(self):
    '''
    Inserts "zu" into infinitives with separable prefixes
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^imp>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"]).project("input")
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
          #  pynini.accep("<Base_Stems>"),
          #  alphabet.closure(),
          #  pynini.cross("<^zz>", ""),
          #  alphabet.closure()
          #  ),
          c2
          + pynini.accep("<Pref_Stems>")
          + alphabet.closure()
          + pynini.accep("<Base_Stems>")
          + pynini.cross("", "z u")
          + alphabet.closure()
          + pynini.cross("<^zz>", "")
          + alphabet.closure()
          ).optimize()

  def __construct_imperative_filter(self):
    '''
    Imperatives have no separable prefixes
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoHy>", "<NoDef>", "<VADJ>", "<CB>", "<FB>", "<UL>", "<SS>", "<DEL-S>", "<Low#>", "<Up#>", "<Fix#>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>"]).project("input")
          ).optimize()

      c2 = pynini.union(
          alphabet,
          pynini.cross(self.__syms.stem_types, "<CB>")
          ).closure().optimize()

      return pynini.union(
          c2,
          pynini.cross("<Base_Stems>", "<CB>")
          + alphabet.closure()
          + pynini.cross("<^imp>", "")
          + alphabet.closure()
          ).optimize()

  def __construct_uplow(self):
    '''
    Upper/Lower case markers
    '''
    with pynini.default_token_type(self.__syms.alphabet):

      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<n>", "<~n>", "<e>", "<d>", "<NoDef>", "<FB>", "<UL>", "<SS>", "<DEL-S>",  "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<^imp>", "<ge>", "<^zz>"]).project("input")
          ).optimize()
      
      s = pynini.concat(
          alphabet,
          pynini.union(
            alphabet,
            pynini.accep("<CB>")
            ).closure()
          ).optimize()

      s2 = pynini.concat(
          pynini.union(
            pynini.concat(
              pynini.cross("<CB>", ""),
              self.__syms.characters_upper
              ),
            pynini.concat(
              pynini.cross("<CB>", "").closure(0, 1),
              self.__syms.characters_lower
              )
            ),
          s
          ).optimize()

      return pynini.union(
          pynini.concat(
            pynini.cross("<^UC>", ""),
            pynini.concat(
              pynini.string_map(["<NoDef>", "<NoHy>"]).project("input").closure(0, 1),
              pynini.concat(
                pynini.cross("", "<^UC>"),
                pynini.concat(
                  s2,
                  pynini.cross("<Low#>", "")
                  )
                )
              )
            ),
          pynini.concat(
            pynini.accep("<NoHy>").closure(0, 1),
            pynini.union(
              pynini.concat(
                pynini.cross("<CB>", ""),
                pynini.concat(
                  s,
                  pynini.cross("<Fix#>", "")
                  )
                ),
              pynini.concat(
                pynini.cross(pynini.string_map(["<CB>", "<epsilon>"]).project("input"), "<^UC>"),
                pynini.concat(
                  s,
                  pynini.cross("<Up#>", "")
                  )
                ),
              pynini.concat(
                pynini.cross(pynini.string_map(["<CB>", "<epsilon>"]).project("input"), "<CB>"),
                pynini.concat(
                  s,
                  pynini.cross("<Low#>", "")
                  )
                )
              )
            )
          ).optimize()
