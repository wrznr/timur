# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class InflectionFst:
  '''
  Define the inflection paradigm
  '''

  def __init__(self,syms):

    #
    # store alphabet
    #
    self.__syms = syms

    #
    # case markers
    #
    fix       = pynini.transducer("", "<Fix#>", output_token_type=syms.alphabet)
    adj       = pynini.transducer("", "<Low#>", output_token_type=syms.alphabet)
    adj_up    = pynini.transducer("", "<Up#>", output_token_type=syms.alphabet)
    n         = pynini.transducer("", "<Up#>", output_token_type=syms.alphabet)
    n_low     = pynini.transducer("", "<Low#>", output_token_type=syms.alphabet)
    v         = pynini.transducer("", "<Low#>", output_token_type=syms.alphabet)
    closed    = pynini.transducer("", "<Low#>", output_token_type=syms.alphabet)
    closed_up = pynini.transducer("", "<Up#>", output_token_type=syms.alphabet)

    #
    # inflection classes
    #

    #
    # abbreviations
    abk_ADJ = pynini.concat(
        pynini.transducer("<^ABK> <+ADJ>", "", input_token_type=syms.alphabet),
        adj
        )
    abk_ADV = pynini.concat(
        pynini.transducer("<^ABK> <+ADV>", "", input_token_type=syms.alphabet),
        closed
        )
    abk_ART = pynini.concat(
        pynini.transducer("<^ABK> <+ART>", "", input_token_type=syms.alphabet),
        closed
        )
    abk_DPRO = pynini.concat(
        pynini.transducer("<^ABK> <+DEMPRO>", "", input_token_type=syms.alphabet),
        closed
        )
    abk_KONJ = pynini.concat(
        pynini.transducer("<^ABK> <+KONJ>", "", input_token_type=syms.alphabet),
        closed
        )
    abk_NE = pynini.concat(
        pynini.transducer("<^ABK> <+NE>", "", input_token_type=syms.alphabet),
        n
        )
    abk_NE_Low = pynini.concat(
        pynini.transducer("<^ABK> <+NE>", "", input_token_type=syms.alphabet),
        n_low
        )
    abk_NN = pynini.concat(
        pynini.transducer("<^ABK> <+NN>", "", input_token_type=syms.alphabet),
        n
        )
    abk_NN_Low = pynini.concat(
        pynini.transducer("<^ABK> <+NN>", "", input_token_type=syms.alphabet),
        n_low
        )
    abk_PREP = pynini.concat(
        pynini.transducer("<^ABK> <+PREP>", "", input_token_type=syms.alphabet),
        closed
        )
    abk_VPPAST = pynini.concat(
        pynini.transducer("<^ABK> <^VPPAST> <+ADJ>", "", input_token_type=syms.alphabet),
        adj
        )
    abk_VPPRES = pynini.concat(
        pynini.transducer("<^ABK> <^VPPRES> <+ADJ>", "", input_token_type=syms.alphabet),
        adj
        )

    #
    # adjectives

    # invariant adjectives
    self.__adj0 = pynini.concat(
        pynini.transducer("<+ADJ> <Invar>", "", input_token_type=syms.alphabet),
        adj
        )
    self.__adj0_up = pynini.concat(
        pynini.transducer("<+ADJ> <Invar>", "", input_token_type=syms.alphabet),
        adj_up
        )

    # inflectional endings
    adj_flex_suff = pynini.union(
        pynini.concat(
          pynini.transducer("<Masc> <Nom> <Sg> <St/Mix>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Masc> <Nom> <Sg> <Sw>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Masc> <Gen> <Sg>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Masc> <Dat> <Sg> <St>", "e m", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Masc> <Dat> <Sg> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Masc> <Akk> <Sg>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Fem> <Nom> <Sg>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Fem> <Gen> <Sg> <St>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Fem> <Gen> <Sg> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Fem> <Dat> <Sg> <St>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Fem> <Dat> <Sg> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Fem> <Akk> <Sg>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<Neut> <Nom> <Sg> <St/Mix>", "e s", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
            pynini.transducer("<Neut> <Nom> <Sg> <Sw>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<Neut> <Gen> <Sg>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<Neut> <Dat> <Sg> <St>", "e m", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<Neut> <Dat> <Sg> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<Neut> <Akk> <Sg> <St/Mix>", "e s", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<Neut> <Akk> <Sg> <Sw>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<NoGend> <Nom> <Pl> <St>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<NoGend> <Nom> <Pl> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<NoGend> <Gen> <Pl> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<NoGend> <Gen> <Pl> <St>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<NoGend> <Dat> <Pl>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<NoGend> <Akk> <Pl> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            ),
        pynini.concat(
            pynini.transducer("<NoGend> <Akk> <Pl> <St>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            adj
            )
        ).optimize()

    # inflectional endings for nominalization
    adj_nn_suff = pynini.union(
        pynini.concat(
          pynini.transducer("<+NN> <Masc> <Nom> <Sg> <St/Mix>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Masc> <Nom> <Sg> <Sw>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Masc> <Gen> <Sg>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Masc> <Dat> <Sg> <St>", "e m", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Masc> <Dat> <Sg> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Masc> <Akk> <Sg>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Fem> <Nom> <Sg>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Fem> <Gen> <Sg> <St>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Fem> <Gen> <Sg> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Fem> <Dat> <Sg> <St>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Fem> <Dat> <Sg> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Fem> <Akk> <Sg>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<+NN> <Neut> <Nom> <Sg> <St/Mix>", "e s", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
            pynini.transducer("<+NN> <Neut> <Nom> <Sg> <Sw>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <Neut> <Gen> <Sg>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <Neut> <Dat> <Sg> <St>", "e m", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <Neut> <Dat> <Sg> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <Neut> <Akk> <Sg> <St/Mix>", "e s", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <Neut> <Akk> <Sg> <Sw>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <NoGend> <Nom> <Pl> <St>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <NoGend> <Nom> <Pl> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <NoGend> <Gen> <Pl> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <NoGend> <Gen> <Pl> <St>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <NoGend> <Dat> <Pl>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <NoGend> <Akk> <Pl> <Sw/Mix>", "e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            ),
        pynini.concat(
            pynini.transducer("<+NN> <NoGend> <Akk> <Pl> <St>", "e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
            n
            )
        ).optimize()

    # positive
    adj_pos = pynini.union(
        pynini.concat(
          pynini.transducer("<+ADJ> <Pos> <Pred>", "", input_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Pos> <Adv>", "", input_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Pos>", "", input_token_type=syms.alphabet),
          adj_flex_suff
          ),
        ).optimize()

    adj_pos_attr = pynini.concat(
        pynini.transducer("<+ADJ> <Pos>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
        adj_flex_suff
        ).optimize()

    adj_pos_pred = pynini.concat(
        pynini.transducer("<+ADJ> <Pos> <Pred>", "", input_token_type=syms.alphabet),
        adj
        )

    # superlative
    adj_sup = pynini.union(
        pynini.concat(
          pynini.transducer("<+ADJ> <Sup> <Pred>", "s t e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Sup> <Pred>", "s t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Sup> <Adv>", "s t e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Sup>", "s t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj_flex_suff
          ),
        ).optimize()

    # comparative
    adj_comp = pynini.union(
        pynini.concat(
          pynini.transducer("<+ADJ> <Comp> <Pred>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Comp> <Adv>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Comp>", "e r", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj_flex_suff
          ),
        ).optimize()

    # inflection classes (?)
    adj_nn = adj_pos_pred

    self.__adj_plus = pynini.union(
        pynini.concat(
          pynini.transducer("", "<FB>", output_token_type=syms.alphabet),
          adj_pos
          ),
        pynini.concat(
          pynini.transducer("", "<FB>", output_token_type=syms.alphabet),
          adj_comp
          ),
        pynini.concat(
          pynini.transducer("", "<FB>", output_token_type=syms.alphabet),
          adj_sup
          )
        ).optimize()

    adj_pos_sup = pynini.union(
        pynini.concat(
          pynini.transducer("", "<FB>", output_token_type=syms.alphabet),
          adj_pos_attr
          ),
        pynini.concat(
          pynini.transducer("", "<FB>", output_token_type=syms.alphabet),
          adj_sup
          )
        ).optimize()

    adj_umlaut = pynini.union(
        pynini.concat(
          pynini.transducer("", "<FB>", output_token_type=syms.alphabet),
          adj_pos
          ),
        pynini.concat(
          pynini.transducer("", "<UL>", output_token_type=syms.alphabet),
          adj_comp
          ),
        pynini.concat(
          pynini.transducer("", "<UL>", output_token_type=syms.alphabet),
          adj_sup
          )
        ).optimize()

    adj_umlaut_e = pynini.union(
        pynini.concat(
          pynini.transducer("", "<FB>", output_token_type=syms.alphabet),
          adj_pos
          ),
        pynini.concat(
          pynini.transducer("", "<UL>", output_token_type=syms.alphabet),
          adj_comp
          ),
        pynini.concat(
          pynini.transducer("", "<UL> e", output_token_type=syms.alphabet),
          adj_sup
          )
        ).optimize()

    adj_ss_e = pynini.union(
        pynini.concat(
          pynini.transducer("", "<SS> <FB>", output_token_type=syms.alphabet),
          adj_pos
          ),
        pynini.concat(
          pynini.transducer("", "<SS> <FB>", output_token_type=syms.alphabet),
          adj_comp
          ),
        pynini.concat(
          pynini.transducer("", "<SS> <FB> e", output_token_type=syms.alphabet),
          adj_sup
          )
        ).optimize()

    #
    # nouns
    #
 
    #
    # inflection classes

    #
    # inflection endings: atomic

    # Frau; Mythos; Chaos
    n_sg_0 = pynini.union(
        pynini.concat(
          pynini.transducer("<Nom> <Sg>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Gen> <Sg>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Dat> <Sg>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Akk> <Sg>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          )
        ).optimize()

    # Haus-es, Geist-(e)s
    n_sg_es = pynini.union(
        pynini.concat(
          pynini.transducer("<Nom> <Sg>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Gen> <Sg>", "<FB> e s <^Gen>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Dat> <Sg>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Dat> <Sg>", "<FB> e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Akk> <Sg>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          )
        ).optimize()

    n_pl_0 = pynini.union(
        pynini.concat(
          pynini.transducer("<Nom> <Pl>", "", input_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Gen> <Pl>", "", input_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Dat> <Pl>", "n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Akk> <Pl>", "", input_token_type=syms.alphabet),
          n
          )
        ).optimize()

    n_pl_x = pynini.union(
        pynini.concat(
          pynini.transducer("<Nom> <Pl>", "", input_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Gen> <Pl>", "", input_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Dat> <Pl>", "", input_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Akk> <Pl>", "", input_token_type=syms.alphabet),
          n
          )
        ).optimize()


    #
    # inflection endings: meta
    n_es_e = pynini.union(
        n_sg_es,
        pynini.concat(
          pynini.transducer("", "<FB> e", output_token_type=syms.alphabet),
          n_pl_0
          )
        )
    n_es_en = pynini.union(
        n_sg_es,
        pynini.concat(
          pynini.transducer("", "<FB> e n", output_token_type=syms.alphabet),
          n_pl_x
          )
        )
    n_0_en = pynini.union(
        n_sg_0,
        pynini.concat(
          pynini.transducer("", "<FB> e n", output_token_type=syms.alphabet),
          n_pl_0
          )
        )

    # NMasc_es_e: Tag-(e)s/Tage
    self.__nmasc_es_e = pynini.concat(
        pynini.transducer("<+NN> <Masc>", "", input_token_type=syms.alphabet),
        n_es_e
        ).optimize()

    # NMasc_es_en: Fleck-(e)s/Flecken
    self.__nmasc_es_en = pynini.concat(
        pynini.transducer("<+NN> <Masc>", "", input_token_type=syms.alphabet),
        n_es_en
        ).optimize()

    # NFem-Deriv
    self.__nfem_deriv = pynini.concat(
        pynini.transducer("<+NN> <Fem>", "", input_token_type=syms.alphabet),
        n_0_en
        ).optimize()

    #
    # building the inflection transducer
    #
    self.__inflection = self.__construct_inflection()

    #
    # definition of a filter which enforces the correct inflection
    #
    self.__inflection_filter = self.__construct_inflection_filter()

  @property
  def inflection(self):
    '''
    Return the inflection transducer 
    '''
    return self.__inflection

  @property
  def inflection_filter(self):
    '''
    Return the complete inflection filter 
    '''
    return self.__inflection_filter

  def __construct_inflection(self):
    '''
    Build the inflection transducer
    '''
    return pynini.union(
        pynini.concat(
          pynini.transducer("", "<Adj0>", output_token_type=self.__syms.alphabet),
          self.__adj0
          ),
        pynini.concat(
          pynini.transducer("", "<Adj0-Up>", output_token_type=self.__syms.alphabet),
          self.__adj0_up
          ),
        pynini.concat(
          pynini.transducer("", "<Adj+>", output_token_type=self.__syms.alphabet),
          self.__adj_plus
          ),
        pynini.concat(
          pynini.transducer("", "<NMasc_es_e>", output_token_type=self.__syms.alphabet),
          self.__nmasc_es_e
          ),
        pynini.concat(
          pynini.transducer("", "<NMasc_es_en>", output_token_type=self.__syms.alphabet),
          self.__nmasc_es_en
          ),
        pynini.concat(
          pynini.transducer("", "<NFem-Deriv>", output_token_type=self.__syms.alphabet),
          self.__nfem_deriv
          )
        ).optimize()

  def __construct_inflection_filter(self):
    '''
    Define a filter which enforces the correct inflection
    '''
    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<ge>", "<no-ge>", "<^imp>", "<^zz>", "<^pp>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<Fix#>", "<Low#>", "<Up#>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
        ).project().closure()

    return pynini.concat(
        pynini.union(
          pynini.concat(
            pynini.transducer("<Adj0>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<Adj0>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<Adj0-Up>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<Adj0-Up>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<Adj+>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<Adj+>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NMasc_es_e>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NMasc_es_e>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NMasc_es_en>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NMasc_es_en>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NFem-Deriv>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NFem-Deriv>", "", input_token_type=self.__syms.alphabet)
            )
          ),
        alphabet
        ).optimize()
