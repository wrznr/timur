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
  tokenizer = re.compile("(<[^>]*>|.)(?::(<[^>]*>|.))?", re.U)
  for line in source:
    line = line.strip()
    if line:
      tmp = pynini.Fst()
      tmp.set_input_symbols(symbol_table)
      tmp.set_output_symbols(symbol_table)
      start = tmp.add_state()
      tmp.set_start(start)
      tmp.set_final(start)
      for token in tokenizer.findall(line):
        if token[1]:
          tmp1 = pynini.concat(tmp, pynini.accep(token[0], token_type=symbol_table))
          tmp2 = pynini.concat(tmp, pynini.accep(token[1], token_type=symbol_table))
          tmp = pynini.concat(tmp, pynini.cross(tmp1, tmp2))
        else:
          tmp = pynini.concat(tmp, pynini.accep(token[0], token_type=symbol_table))
      lex = pynini.union(lex, tmp)
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
