from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from sqlalchemy import text

import db_util
from model import search

app = Flask(__name__)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@SocketIO.on(message="query", self=socketio)
def get_optimized_query_socket(query):
    try:
        execution_plan = None
        conn = db_util.get_connection()
        explanation = conn.execute(text('EXPLAIN FORMAT=TREE ' + query))
        for row in explanation:
            execution_plan = row[0]
        conn.close()
        result_df = search(query)
        optimized_queries = result_df["optimized_query"].tolist()
        return {'status': 'success', 'queries': optimized_queries, 'execution_plan': execution_plan}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.route('/optimize', methods=['POST'])
def get_optimized_query():
    try:
        query = request.json['query']
        execution_plan = None
        conn = db_util.get_connection()
        explanation = conn.execute(text('EXPLAIN FORMAT=TREE ' + query))
        for row in explanation:
            execution_plan = row[0]
        conn.close()
        result_df = search(query)
        optimized_queries = result_df["optimized_query"].tolist()
        return {'status': 'success', 'queries': optimized_queries, 'execution_plan': execution_plan}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    app.run()
