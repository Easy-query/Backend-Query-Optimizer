from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import text

import db_util
from model import search

app = Flask(__name__)

CORS('app', origins='http://localhost:4200')


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


@app.route('/optimize', methods=['GET'])
def get_optimized_query():
    get_body = request.get_json()
    query = get_body['query']
    try:
        result_df = search(query)
        # print(result_df)
        optimized_queries = result_df["optimized_query"].tolist()
        return {'status': 'success', 'queries': optimized_queries}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    app.run()
