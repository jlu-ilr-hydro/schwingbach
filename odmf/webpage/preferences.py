'''
Created on 25.09.2012

@author: philkraf
'''
from pathlib import Path
from .auth import expose_for, users
from . import lib as web
import json
from ..config import conf
import traceback

json_in = web.cherrypy.tools.json_in


class Preferences(object):
    exposed = True
    default = {'map': conf.map_default,
               'site': 1,
               }
    types = dict(map=dict(lat=float, lng=float, zoom=int, type=str),
                 site=int)

    def __init__(self):
        #f = None
        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        except Exception as e:
            self.data = Preferences.default

            traceback.print_tb(e.__traceback__)

    @property
    def filename(self):
        if users.current:
            return Path(conf.preferences) / f'{users.current.name}.json'
        else:
            return Path(conf.preferences) / 'any.json'

    def __getitem__(self, item):
        return self.data.get(item)

    def __setitem__(self, item, value):
        self.data.update({item: value})
        self.save()

    def __contains__(self, item):
        return item in self.data

    def save(self):
        with open(self.filename, 'w') as f:
            # string cast needed since as_json returns bytes (due to python3 refactoring measures)
            f.write(web.as_json(self.data))

    @expose_for()
    @web.mime.json
    def index(self, item=''):
        data = self.data
        print("index for preferences")
        #
        # Seems pythons needs still explicit encoding
        if item in data:
            return web.json_out(self.data[item])
        else:
            return web.json_out(self.data)

    @expose_for()
    @json_in()
    def update(self):
        kwargs = web.cherrypy.request.json
        item = kwargs.pop('item', None)
        print('update/', item, kwargs)
        if item:
            value = self.data.setdefault(item, {})
            if hasattr(value, 'update'):
                self.data[item].update(kwargs)
            print(self.data)
        else:
            self.data.update(kwargs)
            print(self.data)
        self.save()
        return self.index()
