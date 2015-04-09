#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from tornado.web import Application
from tornado_eventsource.handler import EventSourceHandler


class EventSourceTestHandler(EventSourceHandler):
    def custom_headers(self):
        return {
            'X-doge-header': 'much head',
            "Transfer-Encoding": 'identity'
        }

    def open(self):
        self.write_message('doge_source', 'much connection')


class EventSourceTestHandlerWithCheckConnectionError(EventSourceHandler):
    def check_connection(self):
        self.error(403)


class EventSourceTestHandlerWithRetry(EventSourceHandler):
    def custom_headers(self):
        return {
            "Transfer-Encoding": 'identity'
        }

    def open(self):
        self.write_message('doge_source', 'such Wow', 300)


class EventSourceTestHandlerWithUrlParam(EventSourceHandler):
    def custom_headers(self):
        return {
            "Transfer-Encoding": 'identity'
        }

    def open(self, param):
        self.write_message('doge_source', 'such Wow %s' % param)


class EventSourceTestHandlerWithoutName(EventSourceHandler):
    def custom_headers(self):
        return {
            "Transfer-Encoding": 'identity'
        }

    def open(self):
        self.write_message(msg='such Wow')


class EventSourceTestHandlerWithMultilineMessage(EventSourceHandler):
    def custom_headers(self):
        return {
            "Transfer-Encoding": 'identity'
        }

    def open(self):
        self.write_message(msg='such Wow\nmuch multi')


class EventSourceTestCase(AsyncHTTPTestCase):

    def get_app(self):
        return Application([
            (r'^/$', EventSourceTestHandler),
            (r'^/forbidden$', EventSourceTestHandlerWithCheckConnectionError),
            (r'^/retry$', EventSourceTestHandlerWithRetry),
            (r'^/param/(\d+)$', EventSourceTestHandlerWithUrlParam),
            (r'^/no_name$', EventSourceTestHandlerWithoutName),
            (r'^/multi_line$', EventSourceTestHandlerWithMultilineMessage),
        ])
