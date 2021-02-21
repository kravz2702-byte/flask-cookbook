from flask import Flask, request

app = Flask(__name__)

@app.route('/a-get-request', methods=['POST', 'GET'])
def get_request():
    if request.method == 'GET':
        bar = request.args.get('foo', 'bar')
    else:
        bar = request.form.get('foo', 'bar')
    return 'A Simple Flask request where foo is %s' % bar