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
        pynini.string_map(["<FB>", "<SS>", "<n>", "<~n>", "<e>", "<d>", "<Ge-Nom>", "<UL>", "<NoHy>", "<NoDef>", "<ge>", "<no-ge>", "<CB>"], input_token_type=syms.alphabet, output_token_type=syms.alphabet).project()
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

    #
    self.__compound_stems_nn = self.__construct_compound_stems_nn(tmp)
    
  
  def __construct_compound_stems_nn(self, tmp):
    '''
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

  @property
  def compound_stems_nn(self):
    '''
    Default compound stems for nouns
    '''
    return self.__compound_stems_nn
