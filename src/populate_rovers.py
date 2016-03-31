"""Initialize database for SQLAlchemy and Pyramid."""
import os
import transaction
import redis
from sqlalchemy import create_engine


from models import (
    DBSession,
    Base,
    Rover,
    Camera
)


def main():
    database_url = os.environ.get("MARS_DATABASE_URL", None)
    engine = create_engine(database_url)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    init_rovers_and_cameras()
    redis_init()


def redis_init():
    redis_url = os.getenv('REDISTOGO_URL', None)
    red = redis.from_url(redis_url)
    red.set('SOL', 0)
    red.set('PAGE', 1)


CAMERAS = {
    'FHAZ': "Front Hazard Avoidance Camera",
    "NAVCAM": "Navigation Camera",
    "MAST": "Mast Camera",
    "CHEMCAM": "Chemistry and Camera Complex",
    "MAHLI": "Mars Hand Lens Imager",
    "MARDI": "Mars Descent Imager",
    "RHAZ": "Rear Hazard Avoidance Camera",
    "PANCAM": "Panoramic Camera",
    "MINITES": "Miniature Thermal Emission Spectrometer (Mini-TES)",
    "ENTRY": "Entry, Descent, and Landing Camera"
}


ROVERS = [
    {'name': 'Curiosity',
     'landing_date': "2012-08-06",
     'cameras': ['FHAZ', "NAVCAM", "MAST", "CHEMCAM", "MAHLI", "MARDI",
                 "RHAZ"],
     'max_date': "2016-03-28",
     'max_sol': 1295,
     'total_photos': 246346,
     },
    {'name': 'Spirit',
     'landing_date': "2004-01-04",
     'cameras': ['FHAZ', "NAVCAM", "RHAZ", "PANCAM", "MINITES", "ENTRY"],
     'max_date': "2010-03-21",
     'max_sol': 2208,
     'total_photos': 124550,
     },
    {'name': 'Opportunity',
     'landing_date': "2004-01-25",
     'max_date': "2016-03-28",
     'cameras': ['FHAZ', "NAVCAM", "RHAZ", "PANCAM", "MINITES", "ENTRY"],
     'max_sol': 4328,
     'total_photos': 178933,
     }
]


def init_rovers_and_cameras():
    """Create all Rovers and Cameras and save in database."""
    camera_list = []
    rover_list = []
    for rover_dict in ROVERS:
        rover_list.append(Rover(**rover_dict))
        rover_name = rover_dict['name']
        cam_list = rover_dict['cameras']
        for short_name in cam_list:
            cam_dict = {
                'name': short_name,
                'rover_name': rover_name,
                'full_name': CAMERAS[short_name]
            }
            camera_list.append(Camera(**cam_dict))
    with transaction.manager:
        DBSession.add_all(camera_list)
        DBSession.add_all(rover_list)
        DBSession.flush()

    posts = DBSession.query(Rover).all()
    print(posts)

if __name__ == '__main__':
    main()
