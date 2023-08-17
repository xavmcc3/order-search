import search_csv

import pandas as pd
import threading
import webview
import random
import time
import sys

class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def set_window(self, window):
        self.window = window

    def init(self):
        response = {
            'message': 'PyWebView Ready'
        }
        return response

    
    def destroy(self):
        self.window.destroy()

    def doSearch(self, data):
        print(data)
        st = time.time()
        results = search_csv.search_for(data[-1], len(data) - 1, max_col=5);
        print(results)

        response = {
            'message': f'search completed in {(st - time.time())}',
            'data': results.to_markdown()
        }
        return response
    

    def doHeavyStuff(self):
        time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
        now = time.time()
        self.cancel_heavy_stuff_flag = False
        for i in range(0, 1000000):
            _ = i * random.randint(0, 1000)
            if self.cancel_heavy_stuff_flag:
                response = {'message': 'Operation cancelled'}
                break
        else:
            then = time.time()
            response = {
                'message': 'Operation took {0:.1f} seconds on the thread {1}'.format((then - now), threading.current_thread())
            }
        return response

    def cancelHeavyStuff(self):
        time.sleep(0.1)
        self.cancel_heavy_stuff_flag = True

    def error(self):
        raise Exception('This is a Python exception')


def main(window: webview.Window):
    pass

if __name__ == "__main__":
    api = Api()
    window = webview.create_window(
        'Woah dude!', './public/index.html',
        width=1000, height=600,
        resizable=False,
        fullscreen=False,
        frameless=True,
        js_api=api,
        )
    
    try:
        api.set_window(window)
        webview.start(main, window, http_server=True)
    except KeyError:
        print("Window closed")
        sys.exit()