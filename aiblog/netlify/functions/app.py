import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app import app
import serverless_wsgi

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)