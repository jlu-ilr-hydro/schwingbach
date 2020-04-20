#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    'render', 'markdown', 'literal', 'user',
    'cherrypy', 'method', 'mime', 'escape',
    'expose', 'json_in', 'HTTPRedirect', 'HTTPError', 'Resource'
]

import cherrypy
from urllib.parse import urlencode

from .renderer import render, Resource, literal, escape
from .render_tools import markdown, user

from .conversion import *

from . import method
from .mime import mime

expose = cherrypy.expose

json_in = cherrypy.tools.json_in

HTTPRedirect = cherrypy.HTTPRedirect
HTTPError = cherrypy.HTTPError

def redirect(url, **kwargs):
    """
    Raises cherrypy.InternalRedirect with the keyword arguments as query string

    eg.

    .. code::

       redirect('/xyz', a=2, b='Hallo')

    redirects to /xyz?a=2&b=Hallo
    """
    qs = urlencode(kwargs)
    return cherrypy.InternalRedirect(url, qs)

def json_out(obj):
    """
    Decorator for exposed functions to convert the output into utf-8 encoded json
    """
    return json.dumps(
        obj,
        sort_keys=True,
        indent=4,
        default=jsonhandler
    ).encode('utf-8')


def show_in_nav_for(level=0, icon=None):
    """
    Use as a class / method decorator to flag an exposed object in the site navigation

    @show_in_nav_for(users.guest)
    @expose
    class SubPage:
        ...
    """
    def decorate(f):
        f.show_in_nav = level
        f.icon = icon
        f.exposed = True
        return f
    return decorate