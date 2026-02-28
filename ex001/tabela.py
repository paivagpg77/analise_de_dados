from IPython.terminal.embed import TerminalInteractiveShell
import pandas as pd

tabela = pd.read_csv("ClientesBanco.csv" , encoding="latin1")
display(tabela)