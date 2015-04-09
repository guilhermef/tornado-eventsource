#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import tornado.web
import tornado.gen as gen
from tornado import httputil
from tornado.iostream import StreamClosedError
import logging


class EventSourceHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request,
                                            **kwargs)
        self.stream = request.connection.stream

    def error(self, status, msg=None):
        raise tornado.web.HTTPError(status)

    def check_connection(self):
        return True

    def custom_headers(self):
        return {}

    def set_default_headers(self):
        default_headers = {
            "Server": "TornadoServer/%s" % tornado.version,
            "Content-Type": "text/event-stream",
            "access-control-allow-origin": "*",
            "connection": "keep-alive",
            "Date": httputil.format_timestamp(time.time()),
        }
        default_headers.update(self.custom_headers())
        self._headers = httputil.HTTPHeaders(default_headers)

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.check_connection()

        self.open(*args, **kwargs)
        self.flush()

    def open(self, *args, **kwargs):
        pass

    def close(self):
        pass

    @gen.coroutine
    def _write(self, message):
        if self.stream.closed():
            return
        try:
            self.write(message)
            yield self.flush()
        except StreamClosedError:
            logging.exception('Stream Closed')
            self.close()

    def write_message(self, name=None, msg=True, wait=None, evt_id=None):
        to_send = ""
        if wait:
            to_send += "\nretry: %s" % wait
        if name:
            to_send += """\nevent: {name}""".format(name=name)
        if evt_id:
            to_send += """\nid: {evt_id}""".format(evt_id=evt_id)
        if isinstance(msg, str) or isinstance(msg, unicode):
            for line in msg.splitlines(False):
                to_send += """\ndata: {msg}""".format(msg=line)
        else:
            to_send += """\ndata: {msg}""".format(msg=msg)
        to_send += "\n\n"
        logging.debug(to_send)
        self._write(to_send)

    def on_connection_close(self):
        self.stream.close()
        self.close()
