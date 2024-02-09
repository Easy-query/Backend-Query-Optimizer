from flask import Flask, request
import sqlglot
from sqlglot.optimizer import optimize

app = Flask(__name__)


@app.route('/ValidateSQL', methods=['GET'])
def validate_query():
    get_body = request.get_json()
    query = get_body['query']
    try:
        sqlglot.transpile(query, read='oracle', pretty='true')
        print(optimize(query))
        return {'status': 'success', 'message': 'Query is valid'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    app.run()
