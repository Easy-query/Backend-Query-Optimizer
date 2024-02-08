from flask import Flask, request
import sqlvalidator

app = Flask(__name__)


@app.route('/ValidateSQL', methods=['GET'])
def validate_query():
    get_body = request.get_json()
    query = get_body['query']
    sql_query = sqlvalidator.parse(query)
    if not sql_query.is_valid():
        return "Invalid SQL Query"
    return "Valid SQL Query"


if __name__ == '__main__':
    app.run()
