from flask import Flask

import utils

app = Flask(__name__)


@app.route('/search/<transaction>')
def search_transaction(transaction):
    return utils.api_search(transaction)


if __name__ == '__main__':
    app.run()
