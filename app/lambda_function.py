from flask import Flask
from .utils import is_open

app = Flask(__name__)

@app.route('/')
def goass():
    if is_open():
        return app.send_static_file('open.html')
    else:
        return app.send_static_file('dicht.html')


if __name__ == '__main__':
 app.run()
