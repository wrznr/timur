import pynini

syms = pynini.SymbolTable.read_text("test.txt")
print(syms.member("<FB>"))
