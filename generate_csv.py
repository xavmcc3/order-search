from dotenv import load_dotenv
from datetime import datetime
from clrprint import clrprint
import openpyxl
import asyncio
import csv
import os

def write_excel_to_csv(excel_path, csv_path):
    clrprint("Serializing", excel_path, end="", clr="w,m")
    print("...")

    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]

    with open(csv_path, 'a', newline="") as f:
        c = csv.writer(f)
        for row in ws.iter_rows(min_row=2, max_col=11):
            if row[0].value == None and row[1].value == None:
                continue
            values = []
            for cell in row:
                values.append(cell.value)
            c.writerow(values)
        f.truncate()
    wb.close()

async def generate_csv(folder_path, csv_path):
    folder = folder_path

    start_time = datetime.now()
    open(csv_path, 'w').close()
    for file in os.listdir(folder):
        if not file.endswith(".xlsx"):
            continue
        if file.startswith("~$"):
            continue
        path = os.path.abspath(os.path.join(folder, file))
        try:
            write_excel_to_csv(path, csv_path)
        except Exception as e:
            clrprint("[ERROR]", "in", path, clr="r,w,m")
            print(e)
    clrprint("[DONE] ", "Operator spreadsheets serialized in ", f"{datetime.now() - start_time}", ".", sep="", clr="g,w,y,w")

if __name__ == "__main__":
    load_dotenv()
    folder = os.getenv("EXCEL_DIR")
    asyncio.run(generate_csv(folder, './res/index.csv'))
