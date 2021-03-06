"""
Starts a cherrypy server
"""
from .. import prefix
from ..config import conf
import cherrypy
from logging import getLogger
import os
import sys
from ..webpage import expose_for

logger = getLogger(__name__)
server_config = {
    'tools.encode.encoding': 'utf-8',
    'tools.encode.on': True,
    'tools.encode.decode': True,
    'server.socket_host': '0.0.0.0',
    'log.access_file': prefix + '/access.log',
    'log.error_file': prefix + '/error.log',
}


def configure_app(autoreload=False):

    static_files = {
        conf.root_url + '/favicon.ico': {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": str(conf.abspath("media/ilr-favicon.png"))
        },
        conf.root_url + '/media': {
            'tools.caching.on': True,
            'tools.caching.delay': 3600
        }
    }

    logger.info(f"autoreload = {autoreload}")
    cherrypy.config.update(server_config)
    cherrypy.config.update({
        'engine.autoreload.on': autoreload,
        'server.socket_port': conf.server_port,
    })
    return static_files


class ProxyRoot:

    exposed=True

    def __init__(self, head_base):
        from ..webpage.root import Root
        self.head_base = head_base
        setattr(self, head_base, Root())

    @expose_for()
    def index(self):
        raise cherrypy.HTTPRedirect('/' + self.head_base)

    def __call__(self, *args, **kwargs):
        r = cherrypy.request
        raise cherrypy.InternalRedirect(conf.root_url)


def start(autoreload=False):
    """
    Creates the root object, compiles the server configuration and starts the server

    Parameters
    ----------
    autoreload: bool
        Set to True to enable autoreloading, that is the server starts again when files are changed

    """
    from ..webpage.root import Root
    if conf.root_url:
        root = ProxyRoot(conf.root_url.replace('/', ''))
    else:
        root = Root()
    logger.info(f'Starting server on http://127.0.0.1:{conf.server_port}{conf.root_url}')
    cherrypy.quickstart(root=root, config=configure_app(autoreload))


def prepare_workdir():
    """
    Starts a cherrypy server, with WORKDIR as the working directory (local ressources and configuration)
    """
    from glob import glob

    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    # System checks !before project imports
    if conf:
        # Check for mandatory attributes
        logger.info("✔ Config is valid")
    else:
        logger.error("Error in config validation")
        logger.error(str(conf.to_dict()))
        return False

    # Start with project imports
    lock_path = prefix + '/sessions'
    
    logger.debug('Ensure subdirectories')
    for d in ['media', 'sessions', 'preferences/plots']:
        os.makedirs(prefix + '/' + d, exist_ok=True)

    logger.debug(f"Kill session lock files in {lock_path}")
    for fn in glob(lock_path + '/*.lock'):
        logger.debug(f'Killing old session lock {fn}')
        os.remove(fn)

    return True
    

