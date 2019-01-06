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
    adj0 = pynini.concat(
        pynini.transducer("<+ADJ> <Invar>", "", input_token_type=syms.alphabet),
        adj
        )
    adj0_up = pynini.concat(
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
