from flask import Flask, request, render_template
import os
import json

app = Flask(__name__)


def es_query(query):
    '''
    Make query to Elasticsearch, rank results by relevance and pagerank together

    :param str query
    :return list: a list of paper dicts (10 is enough)
    :return int: time taken (ms) (given by elasticsearch)
    '''

    ###
    # TODO
    ###

    # TEMP: Just take 10 papers out
    data_path = os.path.join(app.root_path, '..', 'data', 'local', 'filtered_papers.json')
    papers = []
    with open(data_path, encoding='UTF-8') as f:
        count = 0
        for line in f:
            paper_obj = json.loads(line)
            papers.append(paper_obj)
            count += 1
            if count >= 10: break
    return papers, 145


# Home page
@app.route('/', methods=['GET'], strict_slashes=False)
def home_page():
    app.logger.debug('GET /')  # Just a logging example
    return render_template('index.html')


# Result page
@app.route('/result', methods=['GET'], strict_slashes=False)
def result_page():
    query = request.args.get('query', default = '', type = str).strip()

    if query:
        # Search
        papers, time_taken = es_query(query)
        # Process time from ms to s
        time_taken_str = round(time_taken/1000, 2)
        # Process abstract
        for paper in papers:
            abstract = paper['paperAbstract']
            # Truncate abstract
            paper['paperAbstract'] = (abstract[:300] + '...') if len(abstract) > 300 else abstract

            # TODO: add bold to keywords?

    else:
        # Invalid request
        papers = []
        time_taken_str = 0

    # TODO: also render no. of in/out citation?

    return render_template('result.html', query=query, papers=papers, time_taken_str=time_taken_str)


if __name__ == '__main__':
    app.run('0.0.0.0', '8000', debug=True)
