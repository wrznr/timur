# -*- coding: utf-8 -*- 
import pynini


def load_alphabet(source, auto_singletons=True):
    '''
    Load symbols from source and add them to a symbol table.
    '''
    syms = pynini.SymbolTable()
    if auto_singletons:
        for i in range(0,1000):
            symbol = chr(i)
            if symbol.isprintable() and not symbol.isspace():
                syms.add_symbol(symbol)
    for symbol in source:
        if symbol.startswith('#'):
            continue
        syms.add_symbol(symbol.strip())
    return syms

def construct_any(symbol_table):
    '''
    Return an FST for Sigma*.
    '''
    ANY = pynini.Fst()
    sym_it = pynini.SymbolTableIterator(symbol_table)
    start = ANY.add_state()
    ANY.set_start(start)
    ANY.set_final(start)
    while not sym_it.done():
        ANY.add_arc(start, pynini.Arc(symbol_table.find(sym_it.symbol()), symbol_table.find(sym_it.symbol()), 1, start))
        sym_it.next()
    return ANY

def num_fst():
    '''
    Definition of cardinal and ordinal number stems
    '''

    #
    # cardinal number stems
    #
    card_stem_3_9 = pynini.union("drei", "vier", "fünf", "sechs", "sieben", "acht", "neun")
    card_stem_2_9 = pynini.union("zwei", "zwo", card_stem_3_9)
    card_stem_1_9 = pynini.union("eins", card_stem_2_9)
    num_stem_10_19 = pynini.union("zehn", "elf", "zwölf", pynini.concat(card_stem_3_9, "zehn"))
    num_stem_20_90 = pynini.union("dreißig", pynini.concat(pynini.union("zwan", "vier", "fünf", "sech", "sieb", "acht", "neun"), "zig"))

    card_2_99 = pynini.union(
            card_stem_2_9,
            num_stem_10_19,
            pynini.concat(
                pynini.concat(
                    pynini.union("ein", card_stem_2_9), "und"
                    ).closure(0,1),
                num_stem_20_90)
            )
    card_1_99 = pynini.union("eins", card_2_99)

    card_2_999 = pynini.union(
            card_2_99,
            pynini.concat(
                pynini.union("ein", card_stem_2_9).closure(0,1),
                pynini.concat(
                    "hundert",
                    pynini.concat(
                        pynini.acceptor("und").closure(0,1),
                        card_1_99
                        ).closure(0,1)
                    )
                )
            )
    card_1_999 = pynini.union("eins", card_2_999)

    card_2_999999 = pynini.union(
            card_2_999,
            pynini.concat(
                pynini.union("ein", card_2_999).closure(0,1),
                pynini.concat(
                    "tausend",
                    pynini.concat(
                        pynini.acceptor("und").closure(0,1),
                        card_1_999
                        ).closure(0,1)
                    )
                )
            )
    card_base = pynini.union("null", "eins", card_2_999999)
    card_deriv = pynini.union("null", "ein", card_2_999999)

    #
    # ordinal number stems
    #
    ord_stem_3_9 = pynini.union("dritt", "viert", "fünft", "sechst", "siebt", "acht", "neunt")
    ord_stem_1_9 = pynini.union("erst", "zweit", ord_stem_3_9)

    ord_3_99 = pynini.union(
            ord_stem_3_9,
            pynini.concat(num_stem_10_19, "t"),
            pynini.concat(num_stem_20_90, "st"),
            pynini.concat(
                pynini.union("ein", card_stem_2_9),
                pynini.concat(
                    "und",
                    pynini.concat(num_stem_20_90, "st")
                    )
                )
            )
    ord_1_99 = pynini.union("erst", "zweit", ord_3_99)

    ord_3_999 = pynini.union(
            ord_3_99,
            pynini.concat(
                pynini.union("ein", card_stem_2_9).closure(0, 1),
                "hundertst"
                ),
            pynini.concat(
                pynini.union("ein", card_stem_2_9).closure(0, 1),
                pynini.concat(
                    pynini.concat("hundert", pynini.acceptor("und").closure(0, 1)),
                    ord_1_99)
                )
            )
    ord_1_999 = pynini.union("erst", "zweit", ord_3_999)

    ord_3_999999 = pynini.union(
            ord_3_999,
            pynini.concat(
                pynini.union("ein", card_2_999).closure(0, 1),
                pynini.concat(
                    pynini.concat("tausend", pynini.acceptor("und").closure(0, 1)),
                    ord_1_999)
                )
            )
    ord_base = pynini.union("nullt", "erst", "zweit", ord_3_999999)

    #
    # numbers expressed with digits
    #
    dig_card = pynini.string_map([str(x) for x in range(0, 10)]).closure(1)

    

    dig_card.optimize()
    dig_card.draw("test.dot")
    return card_stem_2_9

syms = load_alphabet(open("syms.txt"))

num_stems = num_fst()

ANY = construct_any(syms)

print(syms.member('A'))
