from flask import Flask


app = Flask(__name__)

for bp in all_blueprints:
    app.register_blueprint(bp)