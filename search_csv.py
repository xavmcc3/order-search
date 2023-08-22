from clrprint import clrprint
from datetime import datetime
import pandas as pd

def str_to_time(string):
    return datetime.strptime(string, "%Y-%m-%d")

COLUMN_TYPES = [int, int, None, None, str, str_to_time]

def search_for(path, target, column=0, chunksize=1000, max_col=11):
    results = pd.DataFrame()
    cols = range(0, max_col)
    for chunk in pd.read_csv(
        path,
        encoding="ISO-8859-1",
        chunksize=chunksize,
        usecols=cols,
        header=None
        ):

        df = chunk.fillna(0)
        df[5] = pd.to_datetime(df[5].astype(str), format='mixed', errors="ignore")
        try:
            df[5] = df[5].dt.strftime('%m/%d/%Y %I:%M %p')
        except:
            pass

        target_oftype = COLUMN_TYPES[column](target)
        found = df.loc[df.iloc[:, column] == target_oftype]
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
