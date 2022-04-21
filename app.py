from flask import Flask, abort
from flask_cors import CORS, cross_origin
import json

import utils

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/tx/<transaction>')
@cross_origin()
def search_transaction(transaction):
    search_result = utils.api_search(transaction)
    if not search_result:
        abort(404)
    # тут так по уебски, потому что jsonify из фласка не принимает default
    return app.response_class(
        response=json.dumps(search_result, default=lambda o: o.to_json()),
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run()
