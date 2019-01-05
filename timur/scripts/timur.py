# -*- coding: utf-8 -*- 
from __future__ import absolute_import

from cProfile import Profile
from pstats import Stats

import click
import pynini

from pkg_resources import resource_stream, Requirement

from timur import helpers
from timur import fsts
from timur import symbols

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

    prof = Profile()
    prof.disable()

    syms = symbols.Symbols(helpers.load_alphabet(resource_stream(Requirement.parse("timur"), 'timur/data/syms.txt')))
    print(syms.member("<epsilon>"))
    print(syms.member("!"))
    print(syms.find("!"))

    lex = helpers.load_lexicon(lexicon, syms.alphabet)
    mappings = fsts.MapFst(syms)

    # add repetitive prefixes
    # TODO: move to fst function
    #repeatable_prefs = helpers.concat(
    #    "<Pref_Stems>",
    #    helpers.union(
    #        "u r <PREF>",
    #        "v o r <PREF>",
    #        token_type=syms
    #        ).closure(1),
    #    "<ADJ,NN> <nativ>",
    #    token_type=syms
    #    )
#    lex = pynini.union(lex, repeatable_prefs).optimize()
#    lex.draw("test1.dot")
#
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

    prof.enable()
    deko_filter = fsts.DekoFst(syms)
    prof.disable()
    prof.dump_stats("deko.stats")
    with open('deko_output.txt', 'wt') as output:
        stats = Stats('deko.stats', stream=output)
        stats.sort_stats('cumulative', 'time')
        stats.print_stats()
    deko_filter.suff_filter.draw("suff_phon.dot")

    #pref_filter = fsts.prefix_filter(syms).optimize()
    #pref_filter.draw("pref_phon.dot")

    #compound_filter = fsts.compound_filter(syms).optimize()
    #compound_filter.draw("compound.dot")

    #infix_filter = fsts.infix_filter(syms).optimize()
    #infix_filter.draw("infix.dot")

    #uplow = fsts.uplow(syms)
    #uplow.draw("uplow.dot")
