from flask import Flask
app = Flask(__name__)


from imdb_data import IMDB_DATA
# from flask import jsonify
import json

@app.route('/')
def hello_world():
    # return json.dumps(IMDB_DATA)

    response = app.response_class(
        response=json.dumps(IMDB_DATA),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
