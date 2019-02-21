from flask import Flask
app = Flask(__name__)


from imdb_data import IMDB_DATA

import json

@app.route('/')
def imdb():
    return json.dumps(IMDB_DATA)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
