from flask import Flask, send_from_directory, request

app = Flask(__name__)
STATIC_PATH = './frontend_www/'


# Home page
@app.route('/', methods=['GET'], strict_slashes=False)
def home_page():
    return send_from_directory(STATIC_PATH, 'index.html')


# For js/css/...
@app.route('/static/<path:path>', methods=['GET'], strict_slashes=False)
def static_files(path):
    return send_from_directory(STATIC_PATH, path)


# Result page
@app.route('/result', methods=['GET'], strict_slashes=False)
def result_page():
    query = request.args.get('q', default = '', type = str)

    # TODO

    return send_from_directory(STATIC_PATH, 'result.html')


if __name__ == '__main__':
    app.run('0.0.0.0', '5000', debug=True)
