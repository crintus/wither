# wither

An API that returns the min, max, average and median temperature and humidity for given city and period of time.
Currently only support a 7 day forecast.

# Important
The readme contains local dev via docker, production on heroku and API usage.

There are things I would've liked to add but unfortunately did not get to.
- limiting period to only what is available based on the dataset
- better documentation for the API and a more detailed readme
- more tests to test more success and failed cases

I'm also not super happy about how I designed this and think I could've done better.


# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

I'll share a .env file with Lucian with the API key in.
I'm not protective of it, but it's still an API key and shouldn't go in repos.

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Run tests
If your docker containers are running you can run the test using something like:
```bash
docker exec -it wither_web_1 python manage.py test
```

# Python environment

Everything should be contained in the docker containers.
If packages need to be installed outside, use a virtual environment (I use miniconda):
```bash
conda create --name wither python=3.8
```

# Production (Heroku)
Base url: https://damp-temple-75259.herokuapp.com/api/v1/

# API Usage
## Weather endpoint
Used to see all the available data for a location
```
/api/v1/weather/?location=Cape%20Town
```
No additional filtering other than the location, which is required.


## Weather Summary endpoint
Summarised view of the weather data for location and period specified.
Returns the average, min, max and median for temp and humidity.
Omitting the period will summarise all available data
```
/api/v1/weather/summary/?location=Cape%20Town
```

Providing a period (start and end timestamp) will summarise data for that period.
See weather endpoint for available timestamps
```
/api/v1/weather/summary/?location=Cape%20Town&period=1598176800,1598263200
```