# _*_ Coding: utf-8 _*_
"""Make a live API call and populate the database from the results."""
from __future__ import unicode_literals

import os
import requests
import json
import transaction
from sqlalchemy import create_engine
# from mars_street_view.scripts import initializedb
from models import DBSession, Photo, Base

ROVERS = {
    'Curiosity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    'Opportunity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos',
    'Spirit': 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos',
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


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


def get_one_sol(rover, sol, page):
    results = fetch_photo_data(rover, sol, page)
    if results == 'sol':
        return 'sol'
    populate_from_data(results)
    return 'page'


if __name__ == '__main__':
     get_one_sol('curiosity', 0, 0)
