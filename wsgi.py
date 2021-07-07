"""
We need something that initializes the application running the application
factory and passing the correct value for the parameter config_name. The Flask 
development server can automatically use any file named wsgi.py in the root 
directory, and since WSGI is a standard specification using that makes me sure 
that any HTTP server we will use in production (for example Gunicorn or uWSGI) 
will be immediately working.
"""

import os

from application.app import create_app

app = create_app(os.environ["FLASK_CONFIG"])
# we expect value in {Production, Development, Testing}

