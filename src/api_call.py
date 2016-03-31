# _*_ Coding: utf-8 _*_
# heroku addons:create heroku-postgresql:hobby-basic
#  heroku pg:promote HEROKU_POSTGRESQL_MAROON
"""Make a live API call and populate the database from the results."""
from __future__ import unicode_literals

import os
import requests
import json
import transaction
from models import Photo, Rover
from sqlalchemy import create_engine
from models import DBSession, Base
# from models import DBSession, Base
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)


# Base = declarative_base()

# DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))



ROVERS = {
    'Curiosity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    'Opportunity': 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos',
    'Spirit': 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos',
}
NASA_API_KEY = os.environ.get('NASA_API_KEY')


def fetch_photo_data(rover, sol, page):
    """Make API call to NASA."""
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos'
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
    print('photo_list made: {}'.format(len(photo_list)))
    posts = DBSession.query(Rover).all()
    print(posts)
    with transaction.manager:
        DBSession.add_all(photo_list)
        DBSession.flush()
    # transaction.commit()
    # DBSession.close()
    print('Put to Database')


def get_one_sol(rover, sol, page):
    results = fetch_photo_data(rover, sol, page)
    if results == 'sol':
        return 'sol'
    print('rover:{} sol:{} page:{} result length:{}'.format(rover, sol, page, len(results)))
    populate_from_data(results)
    return 'page'
