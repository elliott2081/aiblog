from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello Railway! 🚂 (NEW CLEAN SETUP)"

@app.route('/about')
def about():
    return "About this blog"

if __name__ == '__main__':
    app.run(debug=True, port=8008)