# a truly minimal HTTP proxy

import SocketServer
import SimpleHTTPServer
import urllib
import cherryproxy
import logging

c = cherryproxy.CherryProxy(log_level=logging.INFO,log_file=True)
c.start()


# PORT = 8000
#
# class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         self.copyfile(urllib.urlopen(self.path), self.wfile)
#
# httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
# print "serving at port", PORT
# httpd.serve_forever()

