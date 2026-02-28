import pandas as pd
df = pd.read_csv('Produto.csv' , encoding='latin1')
media = df['valor'].mean()
print(media)