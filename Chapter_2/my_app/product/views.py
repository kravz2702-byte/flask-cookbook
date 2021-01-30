from flask import render_template, request, Blueprint
from my_app.product.models import MESSAGES

hello = Blueprint('hello', __name__)

@hello.route('/')
@hello.route('/hello')
def hello_world():
    user = request.args.get('user', 'Iron man')
    return render_template('index.html', user = user)
