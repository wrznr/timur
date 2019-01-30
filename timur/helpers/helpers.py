# -*- coding: utf-8 -*- 
import pynini
import re
import json

def load_lexicon(source, symbol_table):
  '''
  Load lexica entries from source interpreting them using a given symbol table.
  '''
  lex = pynini.Fst()
  lex.set_input_symbols(symbol_table)
  lex.set_output_symbols(symbol_table)
  # longest match, prefer complex over simple symbols
  tokenizer = re.compile("<[^>]*>|.", re.U)
  for line in source:
    lex = pynini.union(lex, pynini.acceptor(" ".join(tokenizer.findall(line.strip())), token_type=symbol_table))
  return lex

class Analysis:
  '''
  Analysis wrapper
  '''

  def __init__(self):
    '''
    Constructor
    '''
    self.query = ""
    self.result = ""

  @classmethod
  def spur(cls, path):
    '''
    Create an analysis from a (successful) path
    '''
    a = cls()
    upper = path[0].split(" ")
    lower = path[1].split(" ")

    for i,sym in enumerate(lower):
      if sym == upper[i]:
        a.result += sym
        a.query += sym
      else:
        a.result += "%s:%s" % (upper[i],sym)
        if sym != "<epsilon>":
          a.query += sym
    return a

  def to_json(self):
    '''
    Serialize analysis as JSON
    '''
    return json.dumps(self.__dict__, ensure_ascii=False)
