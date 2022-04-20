from flask import Flask, abort
import json

import utils

app = Flask(__name__)


@app.route('/tx/<transaction>')
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
