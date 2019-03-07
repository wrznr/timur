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

    # superlative with e
    adj_sup_e = pynini.union(
        pynini.concat(
          pynini.transducer("<+ADJ> <Sup> <Pred>", "e s t e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Sup> <Pred>", "e s t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Sup> <Adv>", "e s t e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          adj
          ),
        pynini.concat(
          pynini.transducer("<+ADJ> <Sup>", "e s t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
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

    self.__adj_plus_e = pynini.union(
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
          adj_sup_e
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

    # Opa-s, Klima-s
    n_sg_s = pynini.union(
        pynini.concat(
          pynini.transducer("<Nom> <Sg>", "<FB>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          n
          ),
        pynini.concat(
          pynini.transducer("<Gen> <Sg>", "<FB> s", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
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
    n_es_e_ul = pynini.union(
        n_sg_es,
        pynini.concat(
          pynini.transducer("", "<UL> e", output_token_type=syms.alphabet),
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
          n_pl_x
          )
        )
    n_0_n = pynini.union(
        n_sg_0,
        pynini.concat(
          pynini.transducer("", "<FB> n", output_token_type=syms.alphabet),
          n_pl_x
          )
        )
    n_s_x = pynini.union(
        n_sg_s,
        n_pl_x
        )

    # NMasc_es_e: Tag-(e)s/Tage
    self.__nmasc_es_e = pynini.concat(
        pynini.transducer("<+NN> <Masc>", "", input_token_type=syms.alphabet),
        n_es_e
        ).optimize()

    # NMasc_es_e$: Arzt-(e)s/Ärzte
    self.__nmasc_es_e_ul = pynini.concat(
        pynini.transducer("<+NN> <Masc>", "", input_token_type=syms.alphabet),
        n_es_e_ul
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

    # NFem_0_n: Kammer/Kammern
    self.__nfem_0_n = pynini.concat(
        pynini.transducer("<+NN> <Fem>", "", input_token_type=syms.alphabet),
        n_0_n
        ).optimize()

    # NNeut-Dimin: Mäuschen-s/Mäuschen
    self.__nneut_dimin = pynini.concat(
        pynini.transducer("<+NN> <Neut>", "", input_token_type=syms.alphabet),
        n_s_x
        ).optimize()

    # NNeut/Sg_s: Abitur-s/--
    self.__nneut_sg_s = pynini.concat(
        pynini.transducer("<+NN> <Neut>", "", input_token_type=syms.alphabet),
        n_sg_s
        ).optimize()
    
    #
    # verbs
    #

    #
    # inflection endings: atomic

    # bin's
    v_plus_es = pynini.transducer("/ \' s", "\' s", input_token_type=syms.alphabet, output_token_type=syms.alphabet).closure(0, 1) + v

    # (ich) lerne
    v_pres_reg_1 = pynini.concat(
        pynini.transducer("<+V> <1> <Sg> <Pres> <Ind>", "<FB> e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
        v_plus_es
        ).optimize()

    # (du) lernst
    v_pres_reg_2 = pynini.concat(
        pynini.transducer("<+V> <2> <Sg> <Pres> <Ind>", "<DEL-S> s t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
        v_plus_es
        ).optimize()

    # (er/sie/es) lernt
    v_pres_reg_3 = pynini.concat(
        pynini.transducer("<+V> <3> <Sg> <Pres> <Ind>", "<DEL-S> t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
        v_plus_es
        ).optimize()

    # (wir/ihr/sie) lernen
    v_pres_pl_ind = pynini.concat(
        pynini.union(
          pynini.transducer("<+V> <1> <Pl> <Pres> <Ind>", "<FB> e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <2> <Pl> <Pres> <Ind>", "<DEL-S> t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <3> <Pl> <Pres> <Ind>", "<FB> e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet)
          ),
        v_plus_es
        ).optimize()

    # (ich/du/sie/wir/ihr/sie) lernen
    v_pres_subj = pynini.concat(
        pynini.union(
          pynini.transducer("<+V> <1> <Sg> <Pres> <Konj>", "<FB> e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <2> <Sg> <Pres> <Konj>", "<FB> e s t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <3> <Sg> <Pres> <Konj>", "<FB> e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <1> <Pl> <Pres> <Konj>", "<FB> e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <2> <Pl> <Pres> <Konj>", "<FB> e t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <3> <Pl> <Pres> <Konj>", "<FB> e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet)
          ),
        v_plus_es
        ).optimize()

    # (ich/du/sie/wir/ihr/sie) lernten
    v_past_ind_reg = pynini.concat(
        pynini.union(
          pynini.transducer("<+V> <1> <Sg> <Past> <Ind>", "<DEL-S> t e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <2> <Sg> <Past> <Ind>", "<DEL-S> t e s t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <3> <Sg> <Past> <Ind>", "<DEL-S> t e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <1> <Pl> <Past> <Ind>", "<DEL-S> t e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <2> <Pl> <Past> <Ind>", "<DEL-S> t e t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <3> <Pl> <Past> <Ind>", "<DEL-S> t e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet)
          ),
        v_plus_es
        ).optimize()

    # (wir/ihr/sie) lernten
    v_past_subj_reg = pynini.concat(
        pynini.union(
          pynini.transducer("<+V> <1> <Sg> <Past> <Konj>", "<DEL-S> t e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <2> <Sg> <Past> <Konj>", "<DEL-S> t e s t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <3> <Sg> <Past> <Konj>", "<DEL-S> t e", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <1> <Pl> <Past> <Konj>", "<DEL-S> t e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <2> <Pl> <Past> <Konj>", "<DEL-S> t e t", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
          pynini.transducer("<+V> <3> <Pl> <Past> <Konj>", "<DEL-S> t e n", input_token_type=syms.alphabet, output_token_type=syms.alphabet)
          ),
        v_plus_es
        ).optimize()

    # kommt, schaut!
    v_imp_pl = pynini.concat(
        pynini.transducer("<+V> <Imp> <Pl>", "<DEL-S> t <^imp>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
        v_plus_es
        ).optimize()

    # kommt, schaut!
    v_imp_sg = pynini.concat(
        pynini.transducer("<+V> <Imp> <Sg>", "<DEL-S> <^imp>", input_token_type=syms.alphabet, output_token_type=syms.alphabet),
        v_plus_es
        ).optimize()

    # SMOR: investigate Lernen<+NN>
    v_inf = pynini.union(
        pynini.union(
          pynini.transducer("<+V> <Inf>", "", input_token_type=syms.alphabet),
          pynini.transducer("<+V> <Inf> <zu>", "<^zz>", input_token_type=syms.alphabet, output_token_type=syms.alphabet)
          ) + v,
        pynini.transducer("<V> <CONV>", "", input_token_type=syms.alphabet) + self.__nneut_sg_s,
        )

    # SMOR: investigate lernendes<+ADJ>
    v_ppres = pynini.union(
        pynini.transducer("<+V> <PPres>", "", input_token_type=syms.alphabet),
        pynini.transducer("<+V> <PPres> <zu>", "<^zz>", input_token_type=syms.alphabet, output_token_type=syms.alphabet)
        ) + v

    # SMOR: investigate gelerntes<+ADJ>
    v_ppast = pynini.transducer("<+V> <PPast>", "<^pp>", input_token_type=syms.alphabet, output_token_type=syms.alphabet) + v

    # lernend
    v_inf_plus_ppres = pynini.union(
        v_inf,
        pynini.concat(
          pynini.transducer("", "d", output_token_type=syms.alphabet),
          v_ppres
          )
        ).optimize()

    # lernen
    v_inf_stem = pynini.concat(
        pynini.transducer("", "<FB> e n", output_token_type=syms.alphabet),
        v_inf_plus_ppres
        ).optimize()

    # gelernt
    v_pp_t = pynini.concat(
        pynini.transducer("", "<DEL-S> t", output_token_type=syms.alphabet),
        v_ppast
        ).optimize()

    #
    # inflection endings: meta
    v_flex_pres_1 = pynini.union(
        v_pres_reg_1,
        v_pres_pl_ind,
        v_pres_subj,
        v_imp_pl,
        v_inf_stem
        ).optimize()

    v_flex_pres_reg = pynini.union(
          v_flex_pres_1,
          v_pres_reg_2,
          v_pres_reg_3,
          v_imp_sg
        ).optimize()

    v_flex_reg = pynini.union(
        v_flex_pres_reg,
        v_past_ind_reg,
        v_past_subj_reg,
        v_pp_t
        ).optimize()
    

    #
    # inflection classes

    # VVReg: lernen
    self.__vv_reg = pynini.concat(
        pynini.transducer("e n", "", input_token_type=syms.alphabet),
        v_flex_reg
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
          pynini.transducer("", "<Adj+e>", output_token_type=self.__syms.alphabet),
          self.__adj_plus_e
          ),
        pynini.concat(
          pynini.transducer("", "<NMasc_es_e>", output_token_type=self.__syms.alphabet),
          self.__nmasc_es_e
          ),
        pynini.concat(
          pynini.transducer("", "<NMasc_es_$e>", output_token_type=self.__syms.alphabet),
          self.__nmasc_es_e_ul
          ),
        pynini.concat(
          pynini.transducer("", "<NMasc_es_en>", output_token_type=self.__syms.alphabet),
          self.__nmasc_es_en
          ),
        pynini.concat(
          pynini.transducer("", "<NFem-Deriv>", output_token_type=self.__syms.alphabet),
          self.__nfem_deriv
          ),
        pynini.concat(
          pynini.transducer("", "<NFem_0_n>", output_token_type=self.__syms.alphabet),
          self.__nfem_0_n
          ),
        pynini.concat(
          pynini.transducer("", "<NNeut-Dimin>", output_token_type=self.__syms.alphabet),
          self.__nneut_dimin
          ),
        pynini.concat(
          pynini.transducer("", "<NNeut/Sg_s>", output_token_type=self.__syms.alphabet),
          self.__nneut_sg_s
          ),
        pynini.concat(
          pynini.transducer("", "<VVReg>", output_token_type=self.__syms.alphabet),
          self.__vv_reg
          )
        ).optimize()

  def __construct_inflection_filter(self):
    '''
    Define a filter which enforces the correct inflection
    '''
    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<n>", "<e>", "<d>", "<~n>", "<Ge-Nom>", "<UL>", "<SS>", "<FB>", "<DEL-S>", "<ge>", "<no-ge>", "<^imp>", "<^zz>", "<^pp>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<Fix#>", "<Low#>", "<Up#>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet)
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
            pynini.transducer("<Adj+e>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<Adj+e>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NMasc_es_e>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NMasc_es_e>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NMasc_es_$e>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NMasc_es_$e>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NMasc_es_en>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NMasc_es_en>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NFem-Deriv>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NFem-Deriv>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NFem_0_n>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NFem_0_n>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NNeut-Dimin>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NNeut-Dimin>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<NNeut/Sg_s>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<NNeut/Sg_s>", "", input_token_type=self.__syms.alphabet)
            ),
          pynini.concat(
            pynini.transducer("<VVReg>", "", input_token_type=self.__syms.alphabet),
            pynini.transducer("<VVReg>", "", input_token_type=self.__syms.alphabet)
            )
          ),
        alphabet
        ).optimize()
