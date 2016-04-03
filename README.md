This is the automation for filling the database used by:
[Mars Street View](https://github.com/mars-street-view/mars-street-view)

It is in a separate repository because it needed to be it's own
Heroku application.

The scheduled event is triggered in src/clock.py which calls
worker.py to get values from Redis to perform the API call to
the Mars Rover Image API. That code is from the mars-street-view
repository.
