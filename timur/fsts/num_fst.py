# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

def num_fst(symbol_table):
    '''
    Definition of cardinal and ordinal number stems
    '''

    #
    # cardinal number stems
    #
    und = pynini.acceptor("u n d", token_type=symbol_table)
    card_stem_3_9 = union("drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", token_type=symbol_table)
    card_stem_2_9 = union("zwei", "zwo", card_stem_3_9, token_type=symbol_table)
    card_stem_1_9 = union("eins", card_stem_2_9, token_type=symbol_table)
    num_stem_10_19 = union("zehn", "elf", "zwölf", concat(card_stem_3_9, "zehn", token_type=symbol_table), token_type=symbol_table)
    num_stem_20_90 = union("dreißig", concat(union("zwan", "vier", "fünf", "sech", "sieb", "acht", "neun", token_type=symbol_table), "zig", token_type=symbol_table), token_type=symbol_table)

    card_2_99 = union(
            card_stem_2_9,
            num_stem_10_19,
            concat(
                concat(union("ein", card_stem_2_9, token_type=symbol_table), "und", token_type=symbol_table).closure(0,1),
                num_stem_20_90)
            )
    card_1_99 = union("eins", card_2_99, token_type=symbol_table)

    card_2_999 = union(
            card_2_99,
            concat(
                union("ein", card_stem_2_9, token_type=symbol_table).closure(0,1),
                concat(
                    "hundert",
                    concat(
                        und.closure(0,1),
                        card_1_99, token_type=symbol_table
                        ).closure(0,1),
                    token_type=symbol_table
                    )
                )
            )
    card_1_999 = union("eins", card_2_999, token_type=symbol_table)

    card_2_999999 = union(
            card_2_999,
            concat(
                union("ein", card_2_999, token_type=symbol_table).closure(0,1),
                concat(
                    "tausend",
                    concat(
                        und.closure(0,1),
                        card_1_999, token_type=symbol_table
                        ).closure(0,1),
                    token_type=symbol_table
                    )
                )
            )
    card_base = union("null", "eins", card_2_999999, token_type=symbol_table)
    card_deriv = union("null", "ein", card_2_999999, token_type=symbol_table)

    #
    # ordinal number stems
    #
    ord_stem_3_9 = union("dritt", "viert", "fünft", "sechst", "siebt", "acht", "neunt", token_type=symbol_table)
    ord_stem_1_9 = union("erst", "zweit", ord_stem_3_9, token_type=symbol_table)

    ord_3_99 = union(
            ord_stem_3_9,
            concat(num_stem_10_19, "t", token_type=symbol_table),
            concat(num_stem_20_90, "st", token_type=symbol_table),
            concat(
                union("ein", card_stem_2_9, token_type=symbol_table),
                concat("und", num_stem_20_90, "st", token_type=symbol_table)
                )
            )
    ord_1_99 = union("erst", "zweit", ord_3_99, token_type=symbol_table)

    ord_3_999 = union(
            ord_3_99,
            concat(
                union("ein", card_stem_2_9, token_type=symbol_table).closure(0, 1),
                "hundertst",
                token_type=symbol_table
                ),
            concat(
                union("ein", card_stem_2_9, token_type=symbol_table).closure(0, 1),
                concat(
                    "hundert",
                    und.closure(0, 1),
                    ord_1_99,
                    token_type=symbol_table)
                )
            )
    ord_1_999 = union("erst", "zweit", ord_3_999, token_type=symbol_table)

    ord_3_999999 = union(
            ord_3_999,
            concat(
                union("ein", card_2_999, token_type=symbol_table).closure(0, 1),
                concat("tausend", und.closure(0, 1), ord_1_999, token_type=symbol_table)
                )
            )
    ord_base = union("nullt", "erst", "zweit", ord_3_999999, token_type=symbol_table)

    #
    # numbers expressed with digits
    #
    dig_card = pynini.string_map([str(x) for x in range(0, 10)], input_token_type=symbol_table, output_token_type=symbol_table).closure(1)
    dig_ord = concat(dig_card, ".", token_type=symbol_table)

    #
    # adding morphosyntactic information
    #
    quant_helper = pynini.transducer("<QUANT>", "", input_token_type=symbol_table)
    quant = union(
            concat(card_deriv, quant_helper),
            concat(ord_base, quant_helper),
            concat(dig_card, pynini.acceptor("-").closure(0,1), quant_helper),
            concat(
                union("beid", "mehr", "viel", "dies", "doppel", "ganz", "gegen", token_type=symbol_table),
                quant_helper)
            )

    card_features = pynini.transducer("", "<CARD> <base> <nativ> <Card>",  output_token_type=symbol_table)
    ord_features = pynini.transducer("", "<ORD> <base> <nativ> <Ord>",  output_token_type=symbol_table)
    #
    # resulting base stems
    num_base = concat(
            pynini.transducer("", "<Initial> <Base_Stems>", output_token_type=symbol_table),
            union(
                concat(card_base, card_features),
                concat(dig_card, card_features),
                concat(ord_base, ord_features),
                concat(dig_ord, ord_features)
                )
            )
    
    #
    # resulting deriv stems
    num_deriv = concat(
            pynini.transducer("", "<Deriv_Stems>", output_token_type=symbol_table),
            union(
                concat(card_deriv, "<CARD>", token_type=symbol_table),
                concat(dig_card, "<DIGCARD>", token_type=symbol_table),
                concat(ord_base, "<ORD>", token_type=symbol_table)
                ),
            pynini.transducer("", "<deriv> <nativ>", output_token_type=symbol_table)
            )
    
    #
    # resulting kompos stems
    num_kompos = concat(
            pynini.transducer("", "<Kompos_Stems>", output_token_type=symbol_table),
            ord_base,
            "<ORD>",
            pynini.transducer("", "<deriv> <nativ>", output_token_type=symbol_table),
            token_type=symbol_table
            )
    
    return pynini.union(num_base, num_deriv, num_kompos).optimize()
