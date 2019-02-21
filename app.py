import csv
from datetime import datetime
from flask import Flask, render_template, stream_with_context
from io import StringIO
import meetup.api
from settings import *
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response

app = Flask(__name__)

whitelist_patterns = [pattern.strip() for pattern in MEETUP_EVENT_NAME_WHITELIST.split(",")]

def filter_event_list(events):
    filtered_events = []
    for e in events:
        # Case-insensitive string match
        if any([(p.lower() in e['name'].lower()) for p in whitelist_patterns]):
            filtered_events.append(e)

    return filtered_events

def get_next_event():
    client = meetup.api.Client(MEETUP_API_KEY)

    future_events = client.GetEvents({'group_urlname': MEETUP_GROUP_SLUG, 'status': 'upcoming'}).results
    future_events = filter_event_list(future_events)
    next_event = future_events[0]
    return next_event

@app.route('/')
def homepage():
    pretty_title = MEETUP_GROUP_SLUG.replace('-', ' ')
    return render_template('homepage.html', title=pretty_title)

# Source: https://stackoverflow.com/questions/28011341/create-and-download-a-csv-file-from-a-flask-view
@app.route('/download')
def download_csv():
    client = meetup.api.Client(MEETUP_API_KEY)
    next_event = get_next_event()

    def generate(event_id):
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(('Name', '# of Guests'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        rsvps = client.GetRsvps({'urlname': MEETUP_GROUP_SLUG, 'event_id': event_id, 'rsvp': 'yes'})

        # write each log item
        for rsvp in rsvps.results:
            w.writerow((
                rsvp['member']['name'],
                rsvp['guests'],
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # add a filename
    headers = Headers()
    date = datetime.fromtimestamp(next_event['time'] / 1000).strftime('%Y-%m-%d')
    headers.set('Content-Disposition', 'attachment', filename='{}-civictechto-rsvps.csv'.format(date))

    # stream the response as the data is generated
    return Response(
        stream_with_context(generate(next_event['id'])),
        mimetype='text/csv', headers=headers
    )

if __name__ == '__main__':
    app.run(port=PORT)
