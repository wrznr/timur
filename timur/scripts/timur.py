# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import click
import pynini

from pkg_resources import resource_stream, Requirement

from timur import helpers
from timur import fsts

from timur.fsts import sublexica

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

@click.group()
def cli():
    pass


@cli.command(name="build")
@click.argument('lexicon', type=click.File())
def build(lexicon):

    syms = helpers.load_alphabet(resource_stream(Requirement.parse("timur"), 'timur/data/syms.txt'))
    print(syms.member("<epsilon>"))
    print(syms.member("!"))
    print(syms.find("!"))

    lex = helpers.load_lexicon(lexicon, syms)

    # add repetitive prefixes
    # TODO: move to fst function
    repeatable_prefs = helpers.concat(
        "<Pref_Stems>",
        helpers.union(
            "u r <PREF>",
            "v o r <PREF>",
            token_type=syms
            ).closure(1),
        "<ADJ,NN> <nativ>",
        token_type=syms
        )
#    lex = pynini.union(lex, repeatable_prefs).optimize()
#    lex.draw("test1.dot")
#
#    map1, map2 = fsts.map_fst_map(syms)
#    map2.draw("test.dot")
#
#    lex = pynini.compose(map1, lex).optimize()
#    lex.draw("test2.dot")
#
#    lex = pynini.compose(lex, map2).optimize()
#    lex.draw("test3.dot")
#
#    base_stems = sublexica.base_stems(lex, syms)
#    pref_stems = sublexica.pref_stems(lex, syms)
#    verbal_pref_stems = sublexica.verbal_pref_stems(lex, syms)
#    simplex_suff_stems = sublexica.simplex_suff_stems(lex, syms)
#    quant_suff_stems = sublexica.quant_suff_stems(lex, syms)

    tail = fsts.tail(syms)

    #phon = phon_fst(syms)
    #num_stems = fsts.num_fst(syms)
