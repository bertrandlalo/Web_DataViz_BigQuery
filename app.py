from datetime import datetime
import logging
import os

from dateutil.relativedelta import relativedelta
from flask import Flask
from flask import render_template, jsonify, request
from google.cloud import bigquery

from misc_helpers import write_json, read_json, drop_item
from query_helpers import get_distinct_query, get_aggregator_query, PROJECT_ID

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)


def call_big_query(QUERY, PROJECT_ID):
    client = bigquery.Client(project=PROJECT_ID)
    query_job = client.query(QUERY)  # Make an API request.
    return query_job


@app.route("/")
def render_index():
    return render_template('index.html')


@app.route("/dummies")
def render_dummies():
    return render_template('dummies.html')


@app.route("/bigquery")
def render_bigquery():
    return render_template('bigquery.html')


@app.route('/bigquery/getAvailableFilters', methods=['POST'])
def bigquery_get_available_filters():
    request_json = request.get_json()

    on_change = request_json['on_change']
    filters = request_json['filters']

    if on_change == 'topics':
        # client updated the topics selection
        # we should update the available poles accordingly
        QUERY_DISTINCT_POLES = get_distinct_query(drop_item(filters, key='poles'), ['poles'])
        query_job_poles = call_big_query(QUERY_DISTINCT_POLES, PROJECT_ID)
        # todo: handle the poles being '' or None ..
        available_poles = [{'key': str(pole[0]), 'text': str(pole[0])} for pole in query_job_poles]
        available_topics = filters['topics']
    elif on_change == 'poles':
        # client updated the poles selection
        # we should update the available topics accordingly
        QUERY_DISTINCT_TOPICS = get_distinct_query(drop_item(filters, key='topics'), ['topics_id', 'topics_text'])
        query_job_topics = call_big_query(QUERY_DISTINCT_TOPICS, PROJECT_ID)
        available_topics = [{'key': topic_id, 'text': topic_text} for topic_id, topic_text in query_job_topics]
        available_poles = filters['topics']
    else:  # date
        # client updated the date
        # we should update the available poles and topics accordingly
        filters = {'date': filters['date']}  # don't consider current topic and poles selection (todo: Pap ok?)
        QUERY_DISTINCT_TOPICS = get_distinct_query(filters, ['topics_id', 'topics_text'])
        query_job_topics = call_big_query(QUERY_DISTINCT_TOPICS, PROJECT_ID)
        available_topics = [{'key': topic_id, 'text': topic_text} for topic_id, topic_text in query_job_topics]

        QUERY_DISTINCT_POLES = get_distinct_query(filters, ['poles'])
        query_job_poles = call_big_query(QUERY_DISTINCT_POLES, PROJECT_ID)
        # todo: handle the poles being '' or None ..
        available_poles = [{'key': str(pole[0]), 'text': str(pole[0])} for pole in query_job_poles]

    return jsonify(status='ok', available_topics=available_topics, available_poles=available_poles)


@app.route('/bigquery/getChartData', methods=['POST'])
def bigquery_get_chart_data():
    request_json = request.get_json()
    # todo: use datetime to convert format
    filters = request_json['filters']
    aggregators = request_json['aggregators']

    # filters
    # filters = {'dateRange': {'start': '2017-12-31T23:00:00.000Z', 'end': '2018-01-18T23:00:00.000Z'}, 'topics': [{'key': 'antarctiqu-UX9', 'text': 'Antarctique'}]}

    # aggregators
    # aggregators =  {'x': {'key': 'date', 'text': 'Dates'}, 'y': {'key': 'avg_scores', 'text': 'Averrage scores'}, 'hue': None}
    QUERY = get_aggregator_query(filters, aggregators)

    query_job = call_big_query(QUERY, PROJECT_ID)

    rows = list(query_job.result())  # Waits for query to finish

    # Handle special case where x is a date
    if aggregators['x']['key'] == 'round_date':

        times = [row['x'] for row in rows]
        time = datetime.strptime(min(times), '%Y-%m')
        end = datetime.strptime(max(times), '%Y-%m')
        step = relativedelta(months=1)
        custom_rows = []
        while time <= end:
            time.date()
            str_time = str(time)[:7]  # todo: handle ugly hack
            # look for row with x == str_time
            match = [row for row in rows if row['x'] == str_time]
            if match:
                custom_row = dict(match[0])
                custom_rows.append(custom_row)
            else:
                custom_rows.append({'x': str_time, 'y': None, 'hue': None})
            time += step
        rows = custom_rows

    if aggregators.get('hue') is None:
        labels = [row['x'] for row in rows]
        datasets = [{
            'label': aggregators['y']['text'],
            'data': [row['y'] for row in rows]
        }]
    else:
        hue_labels = list({row['hue'] for row in rows})
        datasets = []
        for hue_label in hue_labels:
            print([row['x'] for row in rows if row['hue'] == hue_label])
            datasets.append({'label': [row['x'] for row in rows if row['hue'] == hue_label],
                             'data': [row['y'] for row in rows if row['hue'] == hue_label]})
        labels = hue_labels

    chart_data = {
        'labels': labels,
        'datasets': datasets,
    }

    logger.info(u"chart_data: {}".format(chart_data))
    logger.info(u"query: {}".format(QUERY))

    return jsonify(status='ok', chart_data=chart_data)


@app.route('/bigquery/uploadClientSelection', methods=['POST'])
def bigquery_upload_client_selection():
    request_json = request.get_json()
    filename = os.path.join('.', 'local_db', '{}.json'.format(request_json["chart_name"].strip()))
    write_json(filename, request_json['client_selection'])
    return jsonify(status='ok')


@app.route('/bigquery/downloadClientSelection', methods=['POST'])
def bigquery_download_client_selection():
    request_json = request.get_json()
    filename = os.path.join('.', 'local_db', '{}.json'.format(request_json["chart_name"].strip()))
    client_selection = read_json(filename)
    return jsonify(status='ok', client_selection=client_selection)


if __name__ == "__main__":
    app.run(debug=True)
