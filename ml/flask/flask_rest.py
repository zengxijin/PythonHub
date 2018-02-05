# pip install flask
# Ctrl + F5
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


@app.route('/')
def index():
    return "test rest"


jsons = [
    {
        'int_type': 1,
        'string_type': u'String value one',
        'boolean_type': False
    },
    {
        'int_type': 2,
        'string_type': u'String value two',
        'boolean_type': True
    }
]


# test for get
# @app.route('/ml/api/v1.0/sim', methods=['GET'])
# def get_api():
#     return jsonify({'types': jsons})


# test for with url params
@app.route('/ml/api/v1.0/sim/<int:id>', methods=['GET'])
def get_api_param(id):
    json = filter(lambda t: t['int_type'] == id, jsons)
    if len(json) == 0:
        abort(404)

    return jsonify({'types': json[0]})


# custom error handler
@app.errorhandler(404)
def not_found(error):
    print error
    return make_response(jsonify({'error': 'not found'}), 404)


@app.route('/ml/api/v1.0/sim', methods=['POST'])
def post_api():
    print request.json
    req = request.json
    params = req['params']
    print params[0]['key']

    return jsonify({'a': '2'})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


