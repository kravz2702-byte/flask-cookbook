from flask import Flask, request

app = Flask(__name__)

@app.route('/a-get-request')
def get_request():
    bar = request.args.get('foo', 'bar')
    return 'A Simple Flask request where foo is %s' % bar