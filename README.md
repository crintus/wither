# wither

[![Build Status](https://travis-ci.org/crintus/wither.svg?branch=master)](https://travis-ci.org/crintus/wither)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

An API that returns the min, max, average and median temperature and humidity for given city and period of time.

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Python environment

Everything should be contained in the docker containers.
If packages need to be installed outside, use a virtual environment (I use miniconda):
```bash
conda create --name wither python=3.8
```