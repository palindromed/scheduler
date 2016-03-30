from __future__ import unicode_literals, print_function
import os
# from latest_api_call import get_one_sol
import redis
import requests
import os
import json
import transaction
from sqlalchemy import create_engine
# from mars_street_view.scripts import
from models import DBSession, Photo, Base

ROVERS = {
    'Curiosity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    'Opportunity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos',
    'Spirit': 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos',
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


def main(rover):
    redis_url = os.getenv('REDISTOGO_URL', None)
    if redis_url is not None:
        red = redis.from_url(redis_url)
    else:
        subject = "Redis Error"
        text = "Could not connect to Redis. Unable to get SOL and page"
        send_mail(subject, text)
    new = os.getenv("NEW_REDIS")
    if new:
        print('new')
        sol = 0
        red.set('SOL', sol)
        page = 1
        red.set('PAGE', page)
        os.environ['NEW_REDIS'] = 'False'
        print(sol, page)
    else:
        sol = int(red.get('SOL'))
        page = int(red.get('PAGE'))
        print(sol, page)
    try:
        # save in label, check to see if sol or page should increase
        to_increase = get_one_sol(sol, page)
        if to_increase == 'sol':
            sol += 1
            # red.set('SOL', sol)
            # red.set('PAGE', 1)
            print(sol, page)
        elif to_increase == 'page':
            page += 1
            red.set('page', page)
            print(sol, page)
        subject = 'Success!!'
        text = "All went well in API call. SOL for call was {} on page {}.".format(sol, page)
        send_mail(subject, text)
        print(sol)
    except requests.exceptions.HTTPError:
        subject = "API Error",
        text = "There was a problem connecting to the API. SOL for call was {} on page {}.".format(sol, page)
        send_mail(subject, text)


def send_mail(subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox683f8d129b354362b092d1be8762ae7e.mailgun.org/messages",
        auth=("api", os.environ.get('MAILGUN_API_KEY')),
        data={"from": "Mars Rover Bot <postmaster@sandbox683f8d129b354362b092d1be8762ae7e.mailgun.org>",
              "to": ["Hannah  <hannahkrager@gmail.com>"],
              "subject": "{}".format(subject),
              "text": "{}".format(text)})


def fetch_photo_data(rover, sol, page): # add page, do we need url and rover?
    """Make API call to NASA."""
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
    lst = []
    found_ids = set()
    params = {
        'sol': sol,
        'page': page,
        'api_key': NASA_API_KEY,
    }
    resp = requests.get(url, params=params)
    print(resp)
    resp.raise_for_status()  # <- This is a no-op if there is no HTTP error
    content, encoding = resp.content, resp.encoding
    photo_data = json.loads(content.decode(encoding))
    photos = photo_data['photos']
    if not photos:
        return 'sol'
    for photo in photos:
        if photo['id'] not in found_ids:
            lst.append(photo)
            found_ids.add(photo['id'])
    print(lst[-1])
    return lst


def populate_from_data(results):
    """Push the given list of photo dictionaries into the database."""
    photo_list = [Photo(**result) for result in results]
    database_url = os.environ.get("MARS_DATABASE_URL", None)
    engine = create_engine(database_url)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        DBSession.add_all(photo_list)
        DBSession.flush()
    photos = DBSession.query(Photo).limit(15)
    print(photos)


def get_one_sol(rover, sol, page):
    print(rover, sol, page)
    results = fetch_photo_data(rover, sol, page)
    if results == 'sol':
        print('sol')
        return 'sol'
    #populate_from_data(results)
    print('page')
    return 'page'


# if __name__ == '__main__':
#     main('curiosity')
