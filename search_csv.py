from clrprint import clrprint
from datetime import datetime
import pandas as pd

def search_for(target, column=0, chunksize=1000, max_col=11):
    results = pd.DataFrame()
    cols = range(0, max_col)
    for chunk in pd.read_csv('./data/index.csv', encoding="ISO-8859-1", chunksize=chunksize, header=None, usecols=cols):
        df = chunk.fillna(0)
        target_type = pd.api.types.infer_dtype(df.iloc[:, column], skipna=True)
        print(pd.Series(target).convert_dtypes(infer_objects=True))

        found = df.loc[df.iloc[:, column] == target]
        results = pd.concat([results, found], ignore_index=True, sort=False)
    return results

if __name__ == "__main__":
    try:
        column = int(input("column: "))
    except Exception as e:
        clrprint("[Error]", f"{e}", sep="", clr="r,w")

    try:
        target = int(input("target: "))
    except Exception as e:
        clrprint("[Error]", f"{e}", sep="", clr="r,w")

    start_time = datetime.now()
    results = search_for(target, column)

    print(results)
    clrprint("[DONE] ", "Search completed in ", f"{datetime.now() - start_time}", ".", sep="", clr="g,w,y,w")
