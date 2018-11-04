# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import click, pynini

from pkg_resources import resource_string, Requirement

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


@cli.command(name="compile")
@click.argument('lexicon', type=click.File())
def compile(lexicon):

    syms = helpers.load_alphabet(resource_string(Requirement.parse("timur"), 'timur/data/syms.txt').decode("utf-8"))

    lex = helpers.load_lexicon(lexicon, syms)

    #phon = phon_fst(syms)
    #phon.draw("test.dot")
    num_stems = fsts.num_fst(syms)

    ANY = construct_any(syms)

    print(syms.member('<QUANT>'))
