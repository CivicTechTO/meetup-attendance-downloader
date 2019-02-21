# Meetup Attendance Downloader

Easily download attendance CSV for the next Meetup event.

This simple web app is helpful for when an event venue needs an attendee
list, and you want them to be able to help themselves.

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

# Copy a configuration file and edit
cp sample.env .env
```

### Configuration

The following things can be set via environment variable (and in the
`.env` file):

- `MEETUP_API_KEY` (required)
- `MEETUP_GROUP_SLUG`: The group to work with. (required) Example:
  `Civic-Tech-Toronto`
- `MEETUP_EVENT_NAME_WHITELIST`. A comma-separated list of strings. This
  will be used to find the next event, via case-insensitive match on
Meetup event titles. Example: `hacknight, hack night`


### Run

```
$ pipenv run python app.py
```

Yay! :tada: :tada: You can now access the app at: http://localhost:5000

<!-- Links -->
   [flask]: http://flask.pocoo.org/docs/1.0/foreword/
   [heroku]: https://www.heroku.com/what
   [bootstrap]: https://getbootstrap.com/docs/4.0/getting-started/introduction/
