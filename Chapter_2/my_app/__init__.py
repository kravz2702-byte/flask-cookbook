from flask import Flask
from my_app.product.views import hello

app = Flask(__name__)
app.register_blueprint(hello)