import plotly.express as px
import pandas as pd

tabela = pd.read_csv('ClientesBanco.csv')
grafico = px.histogram(tabela , x = 'Contatos 12m' , color  = 'Categoria')
grafico.show()