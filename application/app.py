from flask import Flask


def create_app(config_name):

    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config" 
    # maps to class from config.py
    # I don't see how it knows about config.py, maybe after we install as 
    # pkg, its in the applicaton namespace. 

    app.config.from_object(config_module)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    return app
