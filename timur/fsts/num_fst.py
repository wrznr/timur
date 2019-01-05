# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

class NumFst:
  '''
  Definition of cardinal and ordinal number stems
  '''

  def __init__(self, syms):

    #
    # cardinal number stems
    #
    und = pynini.acceptor("u n d", token_type=self.__syms.alphabet)
    card_stem_3_9 = union("drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", token_type=self.__syms.alphabet)
    card_stem_2_9 = union("zwei", "zwo", card_stem_3_9, token_type=self.__syms.alphabet)
    card_stem_1_9 = union("eins", card_stem_2_9, token_type=self.__syms.alphabet)
    num_stem_10_19 = union("zehn", "elf", "zwölf", concat(card_stem_3_9, "zehn", token_type=self.__syms.alphabet), token_type=self.__syms.alphabet)
    num_stem_20_90 = union("dreißig", concat(union("zwan", "vier", "fünf", "sech", "sieb", "acht", "neun", token_type=self.__syms.alphabet), "zig", token_type=self.__syms.alphabet), token_type=self.__syms.alphabet)

    card_2_99 = union(
        card_stem_2_9,
        num_stem_10_19,
        concat(
          concat(union("ein", card_stem_2_9, token_type=self.__syms.alphabet), "und", token_type=self.__syms.alphabet).closure(0,1),
          num_stem_20_90)
        )
    card_1_99 = union("eins", card_2_99, token_type=self.__syms.alphabet)

    card_2_999 = union(
        card_2_99,
        concat(
          union("ein", card_stem_2_9, token_type=self.__syms.alphabet).closure(0,1),
          concat(
            "hundert",
            concat(
              und.closure(0,1),
              card_1_99, token_type=self.__syms.alphabet
              ).closure(0,1),
            token_type=self.__syms.alphabet
            )
          )
        )
    card_1_999 = union("eins", card_2_999, token_type=self.__syms.alphabet)

    card_2_999999 = union(
        card_2_999,
        concat(
          union("ein", card_2_999, token_type=self.__syms.alphabet).closure(0,1),
          concat(
            "tausend",
            concat(
              und.closure(0,1),
              card_1_999, token_type=self.__syms.alphabet
              ).closure(0,1),
            token_type=self.__syms.alphabet
            )
          )
        )
    card_base = union("null", "eins", card_2_999999, token_type=self.__syms.alphabet)
    card_deriv = union("null", "ein", card_2_999999, token_type=self.__syms.alphabet)

    #
    # ordinal number stems
    #
    ord_stem_3_9 = union("dritt", "viert", "fünft", "sechst", "siebt", "acht", "neunt", token_type=self.__syms.alphabet)
    ord_stem_1_9 = union("erst", "zweit", ord_stem_3_9, token_type=self.__syms.alphabet)

    ord_3_99 = union(
        ord_stem_3_9,
        concat(num_stem_10_19, "t", token_type=self.__syms.alphabet),
        concat(num_stem_20_90, "st", token_type=self.__syms.alphabet),
        concat(
          union("ein", card_stem_2_9, token_type=self.__syms.alphabet),
          concat("und", num_stem_20_90, "st", token_type=self.__syms.alphabet)
          )
        )
    ord_1_99 = union("erst", "zweit", ord_3_99, token_type=self.__syms.alphabet)

    ord_3_999 = union(
        ord_3_99,
        concat(
          union("ein", card_stem_2_9, token_type=self.__syms.alphabet).closure(0, 1),
          "hundertst",
          token_type=self.__syms.alphabet
          ),
        concat(
          union("ein", card_stem_2_9, token_type=self.__syms.alphabet).closure(0, 1),
          concat(
            "hundert",
            und.closure(0, 1),
            ord_1_99,
            token_type=self.__syms.alphabet)
          )
        )
    ord_1_999 = union("erst", "zweit", ord_3_999, token_type=self.__syms.alphabet)

    ord_3_999999 = union(
        ord_3_999,
        concat(
          union("ein", card_2_999, token_type=self.__syms.alphabet).closure(0, 1),
          concat("tausend", und.closure(0, 1), ord_1_999, token_type=self.__syms.alphabet)
          )
        )
    ord_base = union("nullt", "erst", "zweit", ord_3_999999, token_type=self.__syms.alphabet)

    #
    # numbers expressed with digits
    #
    dig_card = pynini.string_map([str(x) for x in range(0, 10)], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).closure(1)
    dig_ord = concat(dig_card, ".", token_type=self.__syms.alphabet)

    #
    # adding morphosyntactic information
    #
    quant_helper = pynini.transducer("<QUANT>", "", input_token_type=self.__syms.alphabet)
    quant = union(
        concat(card_deriv, quant_helper),
        concat(ord_base, quant_helper),
        concat(dig_card, pynini.acceptor("-").closure(0,1), quant_helper),
        concat(
          union("beid", "mehr", "viel", "dies", "doppel", "ganz", "gegen", token_type=self.__syms.alphabet),
          quant_helper)
        )

    card_features = pynini.transducer("", "<CARD> <base> <nativ> <Card>",  output_token_type=self.__syms.alphabet)
    ord_features = pynini.transducer("", "<ORD> <base> <nativ> <Ord>",  output_token_type=self.__syms.alphabet)
    #
    # resulting base stems
    self.__num_base = concat(
        pynini.transducer("", "<Initial> <Base_Stems>", output_token_type=self.__syms.alphabet),
        union(
          concat(card_base, card_features),
          concat(dig_card, card_features),
          concat(ord_base, ord_features),
          concat(dig_ord, ord_features)
          )
        ).optimize()

    #
    # resulting deriv stems
    self.__num_deriv = concat(
        pynini.transducer("", "<Deriv_Stems>", output_token_type=self.__syms.alphabet),
        union(
          concat(card_deriv, "<CARD>", token_type=self.__syms.alphabet),
          concat(dig_card, "<DIGCARD>", token_type=self.__syms.alphabet),
          concat(ord_base, "<ORD>", token_type=self.__syms.alphabet)
          ),
        pynini.transducer("", "<deriv> <nativ>", output_token_type=self.__syms.alphabet)
        ).optimize()

    #
    # resulting kompos stems
    self.__num_kompos = concat(
        pynini.transducer("", "<Kompos_Stems>", output_token_type=self.__syms.alphabet),
        ord_base,
        "<ORD>",
        pynini.transducer("", "<deriv> <nativ>", output_token_type=self.__syms.alphabet),
        token_type=self.__syms.alphabet
        ).optimize()
    
    self.__num_stems = pynini.union(self.__num_base, self.__num_deriv, self.__num_kompos).optimize()

  @property
  def num_stems(self):
    '''
    Return numeric stems
    '''
    return self.__num_stems
