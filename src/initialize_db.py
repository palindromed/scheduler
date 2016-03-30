import os
# import transaction

from sqlalchemy import create_engine


from models import (
    DBSession,
    Base,
)


def main():
    database_url = os.environ.get("MARS_DATABASE_URL", None)
    engine = create_engine(database_url)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()
