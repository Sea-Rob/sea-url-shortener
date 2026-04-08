import os
from app import app as flask_app
from asgiref.wsgi import WsgiToAsgi

app = WsgiToAsgi(flask_app)
