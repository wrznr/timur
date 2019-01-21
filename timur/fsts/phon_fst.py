# -*- coding: utf-8 -*- 
from __future__ import absolute_import

import pynini

from timur import symbols

class PhonFst:
  '''
  Phonological and orthographic rules
  '''

  def __init__(self, syms):
    '''
    The constructor
    '''

    #
    # store alphabet
    self.__syms = syms

    #
    # construct single rules
    self.__r0 = self.__construct_r0()
    self.__r19 = self.__construct_r19()
    self.__r21 = self.__construct_r21()
    self.__r21.draw("r21.dot")

    #
    # construct intermediate rules
    self.__t1 = self.__r0
    self.__t6 = pynini.compose(self.__r19, self.__r21).optimize()

    self.__x1 = self.__t1
    self.__x2 = self.__t6

    #
    # result transducer
    self.__phon = pynini.compose(self.__x1, self.__x2).optimize()


  @property
  def phon(self):
    '''
    Return the phon transducer 
    '''
    return self.__phon

  
  def __construct_r0(self):
    '''
    Allomorphs

    i<n>loyal ==> illoyal
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<e>", "<d>", "<CB>", "<FB>", "<UL>", "<DEL-S>", "<SS>", "<WB>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    return pynini.union(
        alphabet,
        pynini.concat(
          pynini.transducer("<n>", "l", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["L", "l"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          ),
        pynini.concat(
          pynini.transducer("<n>", "m", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["B", "b", "M", "m", "P", "p"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          ),
        pynini.concat(
          pynini.transducer("<n>", "n", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["A", "a", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "N", "n", "O", "o", "Q", "q", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "Ä", "ä", "Ö", "ö", "Ü", "ü", "ß"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          ),
        pynini.concat(
          pynini.transducer("<n>", "r", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["R", "r"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          ),
        pynini.concat(
          pynini.transducer("<d>", "d", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "H", "h", "I", "i", "J", "j", "M", "m", "O", "o", "Q", "q", "R", "r", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "Ä", "ä", "Ö", "ö", "Ü", "ü", "ß"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
          )
        ).closure().optimize()
  
  def __construct_r1(self):
    '''
    Umlaut

    Apfel$ ==> Äpfel
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<e>", "<d>", "<CB>", "<FB>", "<UL>", "<DEL-S>", "<SS>", "<WB>", "<^UC>", "<^Ax>", "<^pl>", "<^Gen>", "<^Del>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )
  
  def __construct_r19(self):
    '''
    Eliminate markers
    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<CB>", "<^UC>", "<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    return pynini.union(
        alphabet,
        pynini.transducer(
          pynini.string_map(["<DEL-S>", "<SS>", "<FB>", "<^Gen>", "<^Del>", "<^pl>", "<^Ax>", "<WB>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
          ""
          )
        ).closure().optimize()
  
  def __construct_r21(self):
    '''
    Low to up

    '''

    alphabet = pynini.union(
        self.__syms.characters,
        pynini.string_map(["<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
        )

    # Construction in SFST involves negation (which is expensiv).
    # It looks like we can do better:
    return pynini.push(
        pynini.union(
          alphabet.closure(),
          pynini.concat(
            pynini.transducer("<^UC>", "", input_token_type=self.__syms.alphabet).closure(1),
            pynini.union(
              pynini.string_map(["<NoHy>", "<NoDef>"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project(),
              self.__syms.to_upper
              )
            )
          ).closure(), push_labels=True).optimize()
