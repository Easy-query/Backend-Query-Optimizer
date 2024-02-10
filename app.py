from flask import Flask, request
import sqlglot
from sqlglot.optimizer import optimize
import db_util
from sqlalchemy import text

app = Flask(__name__)


@app.route('/ValidateSQL', methods=['GET'])
def validate_query():
    get_body = request.get_json()
    query = get_body['query']
    try:
        conn = db_util.get_connection()
        explanation = conn.execute(text('EXPLAIN FORMAT=TREE ' + query))
        for row in explanation:
            print(row)
        conn.close()
        return {'status': 'success', 'message': 'Query is valid'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    app.run()
