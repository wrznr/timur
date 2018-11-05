# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import click
import pynini

from pkg_resources import resource_stream, Requirement

from timur import helpers
from timur import fsts

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

    lex = helpers.load_lexicon(lexicon, syms)

    # add repetitive prefixes
    # TODO: move to fst function
    print(syms.member("<Pref_Stems>"))
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
    lex = pynini.union(lex, repeatable_prefs)

    map1 = fsts.map_fst_map1(syms)

    lex = pynini.compose(map1, lex)
    #lex.draw("test.dot")

    #phon = phon_fst(syms)
    #num_stems = fsts.num_fst(syms)
