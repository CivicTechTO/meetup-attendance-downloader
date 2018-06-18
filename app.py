import csv
from datetime import datetime
from flask import Flask, stream_with_context
from io import StringIO
import meetup.api
from settings import *
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response

app = Flask(__name__)

# Source: https://stackoverflow.com/questions/28011341/create-and-download-a-csv-file-from-a-flask-view
@app.route('/')
def download_csv():
    client = meetup.api.Client(MEETUP_API_KEY)

    next_event = client.GetEvents({'group_urlname': MEETUP_GROUP_SLUG, 'status': 'upcoming'}).results[0]

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(('Name', '# of Guests'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        next_event = client.GetEvents({'group_urlname': MEETUP_GROUP_SLUG, 'status': 'upcoming'}).results[0]
        rsvps = client.GetRsvps({'urlname': MEETUP_GROUP_SLUG, 'event_id': next_event['id'], 'rsvp': 'yes'})

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
        stream_with_context(generate()),
        mimetype='text/csv', headers=headers
    )

if __name__ == '__main__':
    app.run(port=PORT)
