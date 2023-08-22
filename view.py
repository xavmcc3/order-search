from generate_csv import generate_csv
from datetime import datetime
import webview
import pathlib
import sys

import search_csv
import asyncio
import time
#import eel

class Api:
    @staticmethod
    def set_window(window: webview.Window):
        Api.window = window

    @staticmethod
    def init():
        path = "";
        with open("./data/dir.txt", "r") as f:
            path = f.read()
            f.close()

        response = {
            'message': 'Search Orders',
            'path': path
        }
        return response

    @staticmethod
    def main():
        pass


    @staticmethod
    def destroy():
        Api.window.destroy()

    @staticmethod
    def doSearch(value, column):
        st = time.time()
        results = search_csv.search_for(value, max(0, column - 1), max_col=6);

        response = {
            'message': f'search completed in {round((time.time() - st) * 100) / 100}s',
            'data': results.to_json(orient='table')
        }
        return response
    
    @staticmethod
    def setFolder():
        prev_path = "";
        with open("./data/dir.txt", "r") as f:
            prev_path = f.read()
            f.close()
        path = Api.window.create_file_dialog(webview.FOLDER_DIALOG, allow_multiple=False)
        if path == None:
            return {
                'message': f'folder change cancelled',
                'path': prev_path
            }
        with open("./data/dir.txt", 'w') as f:
            f.write(path[0])
            f.close()

        response = {
            'message': f'set folder to {path[0]}',
            'path': path[0]
        }
        return response

    @staticmethod
    def getLastModified():
        response = {
            'date': datetime.fromtimestamp(pathlib.Path('./data/index.csv').stat().st_mtime).strftime('%m/%d/%Y %I:%M %p')
        }
        return response

    @staticmethod
    def updateIndex():
        time.sleep(0.1) 
        folder = ""
        start = time.time()
        with open("./data/dir.txt", "r") as f:
            folder = f.read()
            f.close()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(generate_csv(folder))
        loop.close()
        
        response = {
            'message': f'updated index in {datetime.fromtimestamp((time.time() - start)).strftime("%H:%M:%S")}'
        }
        return response

if __name__ == "__main__":
    window = webview.create_window(
        'Order Tool', './public/index.html',
        width=1250, height=800,
        fullscreen=False,
        resizable=False,
        frameless=True,
        js_api=Api,
        )
    
    try:
        Api.set_window(window)
        webview.start(Api.main, window, http_server=True)
    except KeyError:
        print("Window closed")
        sys.exit()