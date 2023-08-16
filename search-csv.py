import pandas as pd

chunksize = 1000
results = pd.DataFrame()
targets = [0]
cols = range(0, 11)
for chunk in pd.read_csv('./data/index.csv', encoding="ISO-8859-1", chunksize=chunksize, header=None, usecols=cols):
    df = chunk.fillna(0)
    results = pd.concat([results, df.loc[df.iloc[:, 0].isin(targets)]], ignore_index=True, sort=False)
print(results)