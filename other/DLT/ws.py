 #pip install Flask-Sockets

from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/echo')
def echo_socket(ws):
    while True:
        try:
            message = ws.receive()
            ws.send(message)
        except:
            ws.send("error")
            
@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    app.run(host=host, port=port, debug=True)
