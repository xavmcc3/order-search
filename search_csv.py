from clrprint import clrprint
from datetime import datetime
import pandas as pd

def str_to_time(string):
    return datetime.strptime(string, "%Y-%m-%d")

COLUMN_TYPES = [int, int, None, None, str, str_to_time]
COLUMN_NAMES = ["Delivery", "CO", "Quantity", "Logos", "Operator", "Date"]

def search_for(path, target, column=0, chunksize=1000, max_col=6):
    results = pd.DataFrame()
    cols = range(0, max_col)
    for chunk in pd.read_csv(
        path,
        encoding="ISO-8859-1",
        chunksize=chunksize,
        usecols=COLUMN_NAMES
        ):

        df = chunk.fillna(0)
        df["Date"] = pd.to_datetime(df["Date"].astype(str), format='mixed', errors="ignore")
        df["Delivery"] = df["Delivery"].astype('int64', errors="ignore")
        df["CO"] = df["CO"].astype('int64', errors="ignore")
        try:
            df["Date"] = df["Date"].dt.strftime('%m/%d/%Y %I:%M %p')
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
    results = search_for('res\index.csv', target, column)

    print(results)
    clrprint("[DONE] ", "Search completed in ", f"{datetime.now() - start_time}", ".", sep="", clr="g,w,y,w")
