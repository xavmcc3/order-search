import webview

def main(window: webview.Window):
    pass

window = webview.create_window(
    'Woah dude!', './public/index.html',
    width=1000, height=600,
    resizable=False,
    fullscreen=False,
    frameless=True
    )

webview.start(main, window, http_server=True)
