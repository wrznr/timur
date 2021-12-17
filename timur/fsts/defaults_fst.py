# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import fsts

class DefaultsFst:
  '''
  Generation of default base, derivation and composition stems
  '''

  def __init__(self, syms, sublexica, deko_filter, inflection, phon):

    #
    # store alphabet
    self.__syms = syms

    with pynini.default_token_type(self.__syms.alphabet):

      #
      # run parts of morphology building (cf. timur_fst)
      tmp = (sublexica.verbal_pref_stems + sublexica.base_stems) @ sublexica.nodef_to_null @ deko_filter.pref_filter
      tmp = (sublexica.base_stems | tmp) @ deko_filter.compound_filter

      # ANY TODO: Move to symbols!
      alphabet = pynini.union(
          syms.characters,
          syms.stem_types,
          pynini.string_map(["<FB>", "<SS>", "<n>", "<~n>", "<e>", "<d>", "<Ge-Nom>", "<UL>", "<NoHy>", "<NoDef>", "<ge>", "<Ge>", "<no-ge>", "<CB>"]).project("input")
          ).closure().optimize()

      tmp = (tmp + inflection.inflection) @ (alphabet + inflection.inflection_filter) @ deko_filter.infix_filter @ deko_filter.uplow

      tmp = ((pynini.cross("", "<WB>") + tmp + pynini.cross("", "<WB>")) @ phon.phon).optimize()

      #
      # default stems

      # create a default composition stem for nouns
      self.__compound_stems_nn = self.__construct_compound_stems_nn(tmp)

      # create a deriv stem for Ge nominalization (Gelerne)
      self.__ge_nom_stems_v = self.__construct_ge_nom_stems_v(tmp)

      # create an adjective base stem from participles
      self.__participle_adj = self.__construct_participle_adj(tmp, sublexica)
      self.__participle_adj.draw("participle_adj.dot", portrait=True)
  
  def __construct_participle_adj(self, tmp, sublexica):
    '''
    Stems for conversion of participles into adjectives
    '''
    with pynini.default_token_type(self.__syms.alphabet):
      alphabet = pynini.union(
          self.__syms.characters,
          pynini.string_map(["<VPART>", "<VPREF>", "<PREF>", "<CONV>", "<SUFF>", "<NN>", "<ADJ>", "<V>", "<FT>"]).project("input")
      ).closure().optimize()

      participle_stem_filter_1 = pynini.compose(
          pynini.concat(
            pynini.concat(
              alphabet,
              pynini.cross("<V>", "<+V>")
              ),
            pynini.concat(
              pynini.accep("<zu>").closure(0, 1),
              pynini.accep("<PPast>")
              )
            ),
          pynini.compose(
            tmp,
            pynini.concat(
              sublexica.nodef_to_null,
              pynini.accep("t")
              )
            )
          ).optimize()

      participle_stem_filter_2 = pynini.compose(
          alphabet
          + pynini.cross("<V>", "<+V>")
          + pynini.accep("<zu>").closure(0, 1)
          + pynini.string_map(["<PPast>", "<PPres>"]).project("input")
          ,
          pynini.compose(
            tmp,
            pynini.concat(
              sublexica.nodef_to_null,
              pynini.accep("e n") | pynini.accep("n d")
              )
            )
          )

      return pynini.concat(
          pynini.cross("", "<Base_Stems>"),
          pynini.union(
            participle_stem_filter_1
            + pynini.cross("", "<ADJ>")
            + pynini.cross("<CONV>", "")
            + pynini.cross("", "<base> <nativ> <Adj+e>")
            ,
            participle_stem_filter_2
            + pynini.cross("", "<ADJ>")
            + pynini.cross("<CONV>", "")
            + pynini.cross("", "<base> <nativ> <Adj+>")
            )
          ).optimize()

    
  
  def __construct_ge_nom_stems_v(self, tmp):
    '''
    Stems for ge nominalization of verbs ("Gejammer")
    '''
    with pynini.default_token_type(self.__syms.alphabet):
      alphabet = pynini.union(
          self.__syms.characters,
          self.__syms.categories,
          pynini.string_map(["<CONV>", "<SUFF>"]).project("input")
      )

      # extract infinitives
      infinitives = pynini.compose(
          pynini.concat(
            pynini.concat(
              self.__syms.characters.closure(1),
              pynini.accep("<PREF>")
              ).closure(),
            pynini.concat(
              alphabet.closure(1),
              pynini.cross(
                "",
                "<+V> <Inf>")
              )
            ),
          tmp
          ).optimize()

      insert_ge = pynini.concat(
          pynini.concat(
            self.__syms.characters.closure(1),
            pynini.accep("<PREF>")
            ).closure(),
          pynini.concat(
            pynini.cross("g e <PREF> <Ge>", ""),
            alphabet.closure(1)
            )
        ).optimize()
      
      inserted_ge = pynini.compose(
          pynini.compose(insert_ge, infinitives).project("input"),
          pynini.union(
            self.__syms.to_lower,
            self.__syms.categories,
            self.__syms.prefix_suffix_marker,
            pynini.accep("<Ge>")
            ).closure()
          ).optimize()

      deriv_stem_filter_ge = pynini.compose(
          pynini.compose(
            pynini.compose(
              pynini.union(
                alphabet,
                pynini.accep("<PREF>"),
                pynini.cross("", "<Ge>")
                ).closure(),
              inserted_ge
              ),
            pynini.union(
              self.__syms.characters,
              pynini.accep("<Ge>"),
              pynini.cross(
                pynini.union(
                  self.__syms.categories,
                  self.__syms.prefix_suffix_marker
                  ),
                ""
                )
              ).closure()
            ),
          pynini.concat(
            pynini.union(
              self.__syms.characters,
              pynini.accep("<Ge>"),
              ).closure(1),
            pynini.cross("e n", "")
            )
          ).optimize()

      return (pynini.cross("", "<Deriv_Stems>") + deriv_stem_filter_ge + pynini.accep("<V>") + pynini.cross("", "<deriv> <nativ>")).optimize()
  
  def __construct_compound_stems_nn(self, tmp):
    '''
    Default noun compounding stems
    '''
    with pynini.default_token_type(self.__syms.alphabet):
      kompos_stems = pynini.compose(
          pynini.concat(
            self.__syms.characters.closure(1),
            pynini.union(
              pynini.cross(
                "",
                pynini.concat(
                  pynini.accep("<+NN>"),
                  pynini.concat(
                    self.__syms.gender,
                    pynini.accep("<Nom> <Sg>")
                    )
                  )
                ),
              pynini.cross(
                "",
                pynini.concat(
                  pynini.accep("<+NN>"),
                  pynini.concat(
                    self.__syms.gender,
                    pynini.accep("<Nom> <Pl>")
                    )
                  )
                )
              )
            ),
          tmp
          )
      return (pynini.cross("", "<Kompos_Stems>") + kompos_stems + pynini.accep("<NN>") + pynini.cross("", "<kompos> <nativ>")).optimize()

  @property
  def participle_adj(self):
    '''
    Default base stems for participle adjectives
    '''
    return self.__participle_adj

  @property
  def ge_nom_stems_v(self):
    '''
    Default deriv stems for ge nominalization of verbs
    '''
    return self.__ge_nom_stems_v

  @property
  def compound_stems_nn(self):
    '''
    Default compound stems for nouns
    '''
    return self.__compound_stems_nn
