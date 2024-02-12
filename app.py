from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import text

import db_util
from model import search

app = Flask(__name__)

CORS(app)


@app.route('/optimize', methods=['POST'])
def get_optimized_query():
    try:
        query = request.json['query']
        execution_plan = None
        optimized_execution_plan = None
        conn = db_util.get_connection()
        explanation = conn.execute(text('EXPLAIN FORMAT=TREE ' + query))
        for row in explanation:
            execution_plan = row[0]
        conn.close()
        result_df = search(query)
        optimized_queries = result_df["optimized_query"].tolist()
        explanation = conn.execute(text('EXPLAIN FORMAT=TREE ' + optimized_queries[0]))
        for row in explanation:
            optimized_execution_plan = row[0]
        return {'status': 'success', 'queries': optimized_queries, 'execution_plan_for_original': execution_plan,
                'execution_plan_for_optimized': optimized_execution_plan}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    app.run()
