from generate_csv import generate_csv
from datetime import datetime
import webview
import pathlib
import sys

import search_csv
import asyncio
import time
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def local_path(relative_path):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    return os.path.join(application_path, relative_path)

def print_around(func):
    def call(*args, **kwargs):
        print("======================================")
        func(*args, **kwargs)
        print("======================================\n")

    return call

@print_around
def fancy_print(msg):
    print(msg)

class Api:
    @staticmethod
    def set_window(window: webview.Window):
        Api.window = window

    @staticmethod
    def get_csv():
        Api.csv = local_path('res\index.csv')
        with open(Api.dirs, 'r') as f:
            data = f.readlines()
            try:
                Api.csv = data[1]
            except IndexError:
                pass
            f.close()

    @staticmethod
    def win_log(msg):
        Api.window.evaluate_js(f'addToLog("{msg}")')

    @staticmethod
    def main(window):
        Api.dirs = local_path('res\dir.txt')
        Api.set_window(window)
        if not os.path.exists(local_path('res\\')):
            os.makedirs(local_path('res\\'))

        try:
            open(Api.dirs, 'x')
        except FileExistsError:
            pass
        Api.get_csv()


    def init(self):
        lines = "";
        with open(local_path(Api.dirs), "r") as f:
            lines = f.readlines()
            f.close()

        try:
            folder  = lines[0]
        except:
            folder = 'missing'

        try:
            csv = lines[1]
        except:
            csv = 'missing'
        
        response = {
            'message': 'Search Orders',
            'path': folder,
            'csv': csv
        }
        return response

    def destroy(self):
        Api.window.destroy()

    def doSearch(self, value, column):
        st = time.time()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            results = search_csv.search_for(Api.csv, value, max(0, column - 1), max_col=6);
        except Exception as e:
            raise e

        response = {
            'message': f'search completed in {round((time.time() - st) * 100) / 100}s',
            'data': results.to_json(orient='table')
        }
        return response
    
    def setFolder(self):
        path = Api.window.create_file_dialog(webview.FOLDER_DIALOG, allow_multiple=False)
        if path == None:
            return { 'message': f'folder change cancelled' }
        
        with open(Api.dirs, 'r') as f:
            data = f.readlines()
            f.close()
        with open(Api.dirs, 'w') as f:
            while len(data) < 1:
                data.append('')
            data[0] = path[0]
            for i in range(len(data)):
                data[i] = data[i].rstrip()
            f.write('\n'.join(data).strip())
            f.close()

        response = {
            'message': f'set folder to {path[0]}',
            'path': path[0]
        }
        return response
    
    def setFile(self):
        file_types = ('CSV Files (*.csv)', 'All files (*.*)')
        path = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        if path == None:
            return { 'message': f'file change cancelled' }
        with open(Api.dirs, 'r') as f:
            data = f.readlines()
            f.close()
        with open(Api.dirs, 'w') as f:
            for i in range(len(data)):
                data[i] = data[i].rstrip()
            while len(data) < 2:
                data.append('')
            data[1] = path[0]
            f.write('\n'.join(data).rstrip())
            f.close()

        Api.get_csv()
        response = {
            'message': f'set file to {path[0]}',
            'path': path[0]
        }
        return response

    def getLastModified(self):
        try:
            date = datetime.fromtimestamp(pathlib.Path(Api.csv).stat().st_mtime).strftime('%m/%d/%Y %I:%M %p')
        except:
            date = "Unavailable"
        response = {
            'date': date
        }
        return response

    def updateIndex(self):
        time.sleep(0.1) 
        folder = ""
        start = time.time()
        with open(Api.dirs, "r") as f:
            folder = f.readlines()
            try:
                folder = folder[0].strip()
            except IndexError:
                return { 'message': str(Exception("No folder to read from")) }
            f.close()

        print(folder)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(generate_csv(folder, Api.csv, output=Api.win_log, check_blanks=False, max_blanks=10))
            loop.close()
        except Exception as e:
            return { 'message': str(e) }
        
        response = {
            'message': f'updated index in {datetime.fromtimestamp((time.time() - start)).strftime("%M:%S")}'
        }
        return response

# Build with `python -m PyInstaller --clean order-search.spec`
# or `python -m PyInstaller --onefile --name=order-search --icon=order-tool.ico --clean --add-data="public/*;public/" --windowed --noconsole view.py`

if __name__ == "__main__":
    html = resource_path("public\index.html")
    window = webview.create_window(
        'Order Tool', html,
        width=1050, height=700,
        fullscreen=False,
        resizable=False,
        frameless=True,
        js_api=Api(),
        )
    
    try:
        webview.start(Api.main, window, http_server=True)
    except (Exception, KeyError, KeyboardInterrupt) as e:
        print("Window closed", e)
        sys.exit()
