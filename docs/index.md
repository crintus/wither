# wither

[![Build Status](https://travis-ci.org/crintus/wither.svg?branch=master)](https://travis-ci.org/crintus/wither)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

An API that returns the min, max, average and median temperature and humidity for given city and period of time.. Check out the project's [documentation](http://crintus.github.io/wither/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```
