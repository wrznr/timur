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
    #self.__r1 = self.__construct_r1()

    #
    # construct intermediate rules
    self.__t1 = self.__r0

    self.__x1 = self.__t1

    #
    # result transducer
    self.__phon = self.__x1


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
          pynini.transducer("<n>", "n", input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet),
          pynini.acceptor("<CB>", token_type=self.__syms.alphabet),
          pynini.string_map(["L", "l"], input_token_type=self.__syms.alphabet, output_token_type=self.__syms.alphabet).project()
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
