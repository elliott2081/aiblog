import sys
import os

# Add the root directory to the Python path
root_dir = os.path.join(os.path.dirname(__file__), '../../')
sys.path.insert(0, root_dir)

try:
    from app import app
    import serverless_wsgi
    
    def handler(event, context):
        return serverless_wsgi.handle_request(app, event, context)
        
except Exception as e:
    def handler(event, context):
        return {
            'statusCode': 500,
            'body': f'Import error: {str(e)}'
        }