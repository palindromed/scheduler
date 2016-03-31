from __future__ import unicode_literals, print_function
import os
import SimpleHTTPServer
import SocketServer
from sqlalchemy import create_engine
from models import DBSession, Base


database_url = os.environ.get("MARS_DATABASE_URL", None)
engine = create_engine(database_url)
DBSession.configure(bind=engine)
Base.metadata.create_all(engine)


PORT = int(os.environ.get("PORT", 5000))

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
