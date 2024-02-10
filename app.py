from flask import Flask, request
import sqlglot
from sqlglot.optimizer import optimize
import db_util

app = Flask(__name__)


@app.route('/ValidateSQL', methods=['GET'])
def validate_query():
    get_body = request.get_json()
    query = get_body['query']
    try:
        sqlglot.transpile(query, read='oracle', pretty='true')
        print(optimize(query))
        conn = db_util.get_connection()
        cursor = conn.cursor()
        cursor.execute('EXPLAIN PLAN FOR ' + query)
        cursor.execute('SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY)')
        for row in cursor:
            print(row)
        cursor.close()
        conn.close()
        return {'status': 'success', 'message': 'Query is valid'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    app.run()
