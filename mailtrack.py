import argparse, logging, sys, datetime, base64
import cherrypy
from cherrypy import tools


PIXEL_GIF_DATA = """
R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
""".strip()

@cherrypy.popargs('tracking_id')
class TrackMail(object):
    @cherrypy.expose
    def index(self, tracking_id):
        logstring = "### [{0}] Tracking ID: {1} was received from {2}".format(
            datetime.datetime.now().isoformat(), 
            tracking_id, 
            cherrypy.request.remote.ip)
        logging.warn(logstring)
        cherrypy.response.headers['Content-Type'] = "image/gif"
        return base64.b64decode(PIXEL_GIF_DATA.encode('ascii'))


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("ip", help="IPV4 address in the form w.x.y.z")
        parser.add_argument("port", help="port number in the range 0-65535", type=int)
        parser.add_argument("logfile", help="Name of the logfile")

        args = parser.parse_args()
        logging.basicConfig(filename=args.logfile, level=logging.DEBUG)

        global_conf = {
            'global': {
                'server.socket_host': args.ip,
                'server.socket_port': args.port,
                'server.protocol_version': 'HTTP/1.1'
            }
        }

        cherrypy.config.update(global_conf)
        cherrypy.quickstart(TrackMail())
    except:
        logging.debug("Exception: " + str(sys.exc_info()[0]))
