# _*_ Coding: utf-8 _*_
"""Make a live API call and populate the database from the results."""
from __future__ import unicode_literals

import os
import requests
import json
import transaction
from models import Photo, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROVERS = {
    'Curiosity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    'Opportunity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos',
    'Spirit': 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos',
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


def fetch_photo_data(rover, sol, camera=None):
    try:
        url = ROVERS[rover]
    except KeyError:
        raise ValueError('Incorrect rover name provided.')
    page = 1
    lst = []
    found_ids = set()
    while True:
        params = {
            'sol': sol,
            'page': page,
            'api_key': NASA_API_KEY,
        }
        if camera:
            params['camera'] = camera
        resp = requests.get(url, params=params)
        if resp.status_code == 400:
            params['camera'] = camera or ''
            print('400 response for {0} {camera} sol {sol} page={page}'
                  ''.format(rover, **params))
            break
        content, encoding = resp.content, resp.encoding
        photo_data = json.loads(content.decode(encoding))
        photos = photo_data['photos']
        if not photos:
            break
        for photo in photos:
            if photo['id'] not in found_ids:
                lst.append(photo)
                found_ids.add(photo['id'])
        page += 1

    return lst


def populate_from_data(results):
    """Push the given list of photo dictionaries into the database."""
    database_url = os.environ.get("MARS_DATABASE_URL", None)
    if database_url is None:
        print('cannot connect to db')
    engine = create_engine(database_url)
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = DBSession()
    photo_list = [Photo(**result) for result in results]
    with transaction.manager:
        session.add_all(photo_list)
    session.commit()
    print('Put to database')
    session.close()


def get_one_sol(rover, sol):
    results = fetch_photo_data(rover, sol)
    print('rover:{} sol:{} result length:{}'.format(rover, sol, len(results)))
    if results:
        populate_from_data(results)
