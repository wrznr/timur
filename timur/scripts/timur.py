# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import sys

from cProfile import Profile
from pstats import Stats

import click
import pynini

from timur import fsts
from timur import helpers

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


@cli.command(name="lookup")
@click.argument('strings', nargs=-1)
@click.option('--fst', '-f', required=True)
def lookup(strings, fst):

    #
    # load a previously built morphological analyser
    #
    timur = fsts.TimurFst()
    loaded = timur.load(fst)

    #
    # analysis
    #

    # read input
    in_strings = []
    if strings and strings[0] == u"-":
        for line in sys.stdin:
            in_strings.append(line.strip())
    elif strings:
        for datum in strings:
            in_strings.append(datum)
    else:
        pass

    # convert
    for string in in_strings:
        items = timur.lookup(string)
        for item in items:
            click.echo("> Analysis")
            analysis = helpers.Analysis.spur(item)
            click.echo(analysis.to_json())

@cli.command(name="build")
@click.argument('lexicon', type=click.File())
@click.option('--fst', '-f')
def build(lexicon, fst):

    prof = Profile()
    prof.enable()

    timur = fsts.TimurFst()

    if timur.build(lexicon):
        click.echo("Successfully built the timur fst from the given lexicon.", err=True)
        if fst:
            timur.dump_fst(fst)
        else:
            sys.stdout.write(timur.dumps())
    else:
        click.echo("Could not build the timur fst from the given lexicon.", err=True)
    
    prof.disable()
    prof.dump_stats("timur.stats")
    with open('timur_output.txt', 'wt') as profile:
        stats = Stats('timur.stats', stream=profile)
        stats.sort_stats('cumulative', 'time')
        stats.print_stats()


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
#    base_stems = sublexica.base_stems(lex, syms)
#    pref_stems = sublexica.pref_stems(lex, syms)
#    verbal_pref_stems = sublexica.verbal_pref_stems(lex, syms)
#    simplex_suff_stems = sublexica.simplex_suff_stems(lex, syms)
#    quant_suff_stems = sublexica.quant_suff_stems(lex, syms)
