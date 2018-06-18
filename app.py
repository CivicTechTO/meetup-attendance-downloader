import csv
from datetime import datetime
from flask import Flask, stream_with_context
from io import StringIO
import meetup.api
from settings import *
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response

app = Flask(__name__)

GROUP_SLUG = 'Civic-Tech-Toronto'

def get_data():
    client = meetup.api.Client(MEETUP_API_KEY)
    upcoming_events = client.GetEvents({'group_urlname': GROUP_SLUG, 'status': 'upcoming'})
    next_event_id = upcoming_events.results[0]['id']
    rsvps = client.GetRsvps({'urlname': GROUP_SLUG, 'event_id': next_event_id, 'rsvp': 'yes'})
    return rsvps.results

# Source: https://stackoverflow.com/questions/28011341/create-and-download-a-csv-file-from-a-flask-view
@app.route('/')
def download_log():
    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(('Name', '# of Guests'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each log item
        for rsvp in get_data():
            w.writerow((
                rsvp['member']['name'],
                rsvp['guests'],
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # add a filename
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='meetup-rsvps.csv')

    # stream the response as the data is generated
    return Response(
        stream_with_context(generate()),
        mimetype='text/csv', headers=headers
    )

if __name__ == '__main__':
    app.run(port=PORT)
