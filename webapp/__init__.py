from flask import Flask, request, render_template

app = Flask(__name__)


# Home page
@app.route('/', methods=['GET'], strict_slashes=False)
def home_page():
    app.logger.debug('GET /')  # Just a logging example
    return render_template('index.html')


# Result page
@app.route('/result', methods=['GET'], strict_slashes=False)
def result_page():
    query = request.args.get('query', default = '', type = str)

    # TODO

    return render_template('result.html')


if __name__ == '__main__':
    app.run('0.0.0.0', '8000', debug=True)
