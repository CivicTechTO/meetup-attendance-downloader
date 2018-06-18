# Meetup Attendance Downloader

A simple app that downloads a CSV of the next upcoming event.

This app is helpful for when an event venue needs an attendee list, and
you want them to be able to help themselves.

## :hammer_and_wrench: Technologies Used

- **Python.** A popular programming language.
- [**Flask.**][flask] Python microframework for web apps.
- [**Bootstrap.**][bootstrap] Front-end framework for building
  responsive, mobile-first sites.
* [**Heroku.**][heroku] A platform for easily deploying applications.

## :computer: Local Development

### Setup

1. Install Python.
1. [Install](http://docs.python-guide.org/en/latest/dev/virtualenvs/#installing-pipenv) `pipenv`.

```
# Copy and modify settings as appropriate
$ cp sample.env .env

# Install dependencies
$ pipenv install
```

### Run

```
$ pipenv run python app.py
```

Yay! :tada: :tada: You can now access the app at: http://localhost:5000

<!-- Links -->
   [flask]: http://flask.pocoo.org/docs/1.0/foreword/
   [heroku]: https://www.heroku.com/what
   [bootstrap]: https://getbootstrap.com/docs/4.0/getting-started/introduction/
