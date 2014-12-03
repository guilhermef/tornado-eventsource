#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from tornado.web import Application
from tornado_eventsource.handler import EventSourceHandler


class EventSourceTestHandler(EventSourceHandler):
    def open(self):
        self.write_message('doge_source', 'much connection')


class EventSourceTestHandlerWithCheckConnectionError(EventSourceHandler):
    def check_connection(self):
        self.error(403, 'Forbidden')


class EventSourceTestHandlerWithRetry(EventSourceHandler):
    def open(self):
        self.write_message('doge_source', 'such Wow', 300)


class EventSourceTestHandlerWithUrlParam(EventSourceHandler):
    def open(self, param):
        self.write_message('doge_source', 'such Wow %s' % param)


class EventSourceTestCase(AsyncHTTPTestCase):

    def get_app(self):
        return Application([
            (r'^/$', EventSourceTestHandler),
            (r'^/forbidden$', EventSourceTestHandlerWithCheckConnectionError),
            (r'^/retry$', EventSourceTestHandlerWithRetry),
            (r'^/param/(\d+)$', EventSourceTestHandlerWithUrlParam),
        ])
