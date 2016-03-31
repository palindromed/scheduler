from __future__ import unicode_literals, print_function
import os
import SimpleHTTPServer
import SocketServer


PORT = int(os.environ.get("PORT", 5000))

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
