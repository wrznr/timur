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


    #
    # run parts of morphology building (cf. timur_fst)
    tmp = (sublexica.verbal_pref_stems + sublexica.base_stems) * sublexica.nodef_to_null * deko_filter.pref_filter
    tmp = (sublexica.base_stems | tmp) * deko_filter.compound_filter

    # ANY TODO: Move to symbols!
    alphabet = pynini.union(
        syms.characters,
        syms.stem_types,
        pynini.string_map(["<FB>", "<SS>", "<n>", "<~n>", "<e>", "<d>", "<Ge-Nom>", "<UL>", "<NoHy>", "<NoDef>", "<ge>", "<Ge>", "<no-ge>", "<CB>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project()
        ).closure().optimize()

    tmp = (tmp + inflection.inflection) * (alphabet + inflection.inflection_filter) * deko_filter.infix_filter * deko_filter.uplow

    tmp = pynini.compose(
        pynini.concat(
          pynini.transducer("", "<WB>", output_token_type=self.__syms.alphabet),
          tmp,
          pynini.transducer("", "<WB>", output_token_type=self.__syms.alphabet),
          ),
        phon.phon
        ).optimize()

    #
    # default stems

    # create a default composition stem for nouns
    self.__compound_stems_nn = self.__construct_compound_stems_nn(tmp)
    self.__compound_stems_surface_nn = self.__construct_compound_stems_surface_nn()

    # create a deriv stem for Ge nominalization (Gelerne)
    self.__ge_nom_stems_v = self.__construct_ge_nom_stems_v(tmp)

    # create an adjective base stem from participles
    self.__participle_adj = self.__construct_participle_adj(tmp, sublexica)
    self.__participle_adj.draw("participle_adj.dot", portrait=True)
  
  def __construct_participle_adj(self, tmp, sublexica):
    '''
    Stems for conversion of participles into adjectives
    '''
    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<VPART>", "<VPREF>", "<PREF>", "<CONV>", "<SUFF>", "<NN>", "<ADJ>", "<V>", "<FT>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
    ).closure().optimize()

    return pynini.concat(
        pynini.transducer("", "<Base_Stems>", output_token_type=self.__syms.alphabet),
        pynini.union(
          pynini.concat(
            pynini.compose(
              pynini.concat(
                alphabet,
                pynini.transducer("<V>", "<+V>", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
                pynini.acceptor("<zu>", token_type=self.__syms.alphabet).closure(0, 1),
                pynini.acceptor("<PPast>", token_type=self.__syms.alphabet)
                ),
              pynini.compose(
                tmp,
                pynini.concat(
                  sublexica.nodef_to_null,
                  pynini.acceptor("t", token_type=self.__syms.alphabet)
                  )
                )
              ),
            pynini.transducer("", "<ADJ>", output_token_type=self.__syms.alphabet),
            pynini.transducer("<CONV>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("", "<base> <nativ> <Adj+e>", output_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.compose(
              pynini.concat(
                alphabet,
                pynini.transducer("<V>", "<+V>", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
                pynini.acceptor("<zu>", token_type=self.__syms.alphabet).closure(0, 1),
                pynini.string_map(["<PPast>", "<PPres>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
                ),
              pynini.compose(
                tmp,
                pynini.concat(
                  sublexica.nodef_to_null,
                  pynini.acceptor("e n", token_type=self.__syms.alphabet) | pynini.acceptor("n d", token_type=self.__syms.alphabet)
                  )
                )
              ),
            pynini.transducer("", "<ADJ>", output_token_type=self.__syms.alphabet),
            pynini.transducer("<CONV>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("", "<base> <nativ> <Adj+>", output_token_type=self.__syms.alphabet)
            )
          )
        ).optimize()

    
  
  def __construct_ge_nom_stems_v(self, tmp):
    '''
    Stems for ge nominalization of verbs ("Gejammer")
    '''
    alphabet = pynini.union(
        self.__syms.characters,
        self.__syms.categories,
        pynini.string_map(["<CONV>", "<SUFF>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
    )

    # extract infinitives
    infinitives = pynini.compose(
        pynini.concat(
          pynini.concat(
              self.__syms.characters.closure(1),
              pynini.acceptor("<PREF>", token_type=self.__syms.alphabet)
            ).closure(),
          alphabet.closure(1),
          pynini.transducer(
            "",
            "<+V> <Inf>", output_token_type=self.__syms.alphabet)
          ),
        tmp
        ).optimize()

    insert_ge = pynini.concat(
        pynini.concat(
          self.__syms.characters.closure(1),
          pynini.acceptor("<PREF>", token_type=self.__syms.alphabet)
          ).closure(),
        pynini.transducer("g e <PREF> <Ge>", "", input_token_type=self.__syms.alphabet),
        alphabet.closure(1)
      ).optimize()
    
    inserted_ge = pynini.compose(
        pynini.compose(insert_ge, infinitives).project(),
        pynini.union(
          self.__syms.to_lower,
          self.__syms.categories,
          self.__syms.prefix_suffix_marker,
          pynini.acceptor("<Ge>", token_type=self.__syms.alphabet)
          ).closure()
        ).optimize()

    return pynini.concat(
        pynini.transducer("", "<Deriv_Stems>", output_token_type=self.__syms.alphabet),
        pynini.compose(
          pynini.compose(
            pynini.compose(
              pynini.union(
                alphabet,
                pynini.acceptor("<PREF>", token_type=self.__syms.alphabet),
                pynini.transducer("", "<Ge>", output_token_type=self.__syms.alphabet)
                ).closure(),
              inserted_ge
              ),
            pynini.union(
              self.__syms.characters,
              pynini.acceptor("<Ge>", token_type=self.__syms.alphabet),
              pynini.transducer(
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
              pynini.acceptor("<Ge>", token_type=self.__syms.alphabet),
              ).closure(1),
            pynini.transducer("e n", "", input_token_type=self.__syms.alphabet)
            )
          ),
        pynini.acceptor("<V>", token_type=self.__syms.alphabet),
        pynini.transducer("", "<deriv> <nativ>", output_token_type=self.__syms.alphabet)
        ).optimize()
 
  def __construct_compound_stems_nn(self, tmp):
    '''
    Default noun compounding stems
    '''
    return pynini.concat(
        pynini.transducer("", "<Kompos_Stems>", output_token_type=self.__syms.alphabet),
        pynini.compose(
          pynini.concat(
            self.__syms.characters.closure(1),
            pynini.union(
              pynini.transducer(
                "",
                pynini.concat(
                  pynini.acceptor("<+NN>", token_type=self.__syms.alphabet),
                  self.__syms.gender,
                  pynini.acceptor("<Nom> <Sg>", token_type=self.__syms.alphabet)
                  )
                ),
              pynini.transducer(
                "",
                pynini.concat(
                  pynini.acceptor("<+NN>", token_type=self.__syms.alphabet),
                  self.__syms.gender,
                  pynini.acceptor("<Nom> <Pl>", token_type=self.__syms.alphabet)
                  )
                )
              )
            ),
          tmp
          ),
        pynini.acceptor("<NN>", token_type=self.__syms.alphabet),
        pynini.transducer("", "<kompos> <nativ>", output_token_type=self.__syms.alphabet)
        ).optimize()
 
  def __construct_compound_stems_surface_nn(self):
    '''
    Default noun compounding stems for lemmatizer
    '''
    del_feats = pynini.union(
        self.__syms.characters,
        pynini.transducer("", "<Kompos_Stems>", output_token_type=self.__syms.alphabet),
        pynini.transducer("", "<kompos> <nativ>", output_token_type=self.__syms.alphabet),
        pynini.acceptor("<NN>", token_type=self.__syms.alphabet)
        ).closure().optimize()
    return (del_feats * self.__compound_stems_nn.copy().project(project_output=True)).optimize()

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

  @property
  def compound_stems_surface_nn(self):
    '''
    Default lemmatizing compound stems for nouns
    '''
    return self.__compound_stems_surface_nn
