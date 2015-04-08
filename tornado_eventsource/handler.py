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
        self._write(
            "HTTP/1.1 %s %s\r\n\r\n" % (status, msg)
        )
        self.stream.close()
        return

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
            "Transfer-Encoding": 'identity',
            "Date": httputil.format_timestamp(time.time()),
        }
        default_headers.update(self.custom_headers())
        self._headers = httputil.HTTPHeaders(default_headers)

    @gen.coroutine
    def _execute(self, transforms, *args, **kwargs):
        if not self.check_connection():
            return

        self.open_args = [self.decode_argument(arg) for arg in args]
        self.open_kwargs = dict((k, self.decode_argument(v, name=k))
                                for (k, v) in kwargs.items())

        start_line = httputil.ResponseStartLine('',
                                                self._status_code,
                                                self._reason)
        # EventSource only supports GET method
        if self.request.method != 'GET':
            self.error(405, 'Method Not Allowed')
        yield self.request.connection.write_headers(start_line, self._headers)

        self.open(*self.open_args, **self.open_kwargs)

    def open(self, *args, **kwargs):
        pass

    def close(self):
        pass

    def _write(self, message):
        if self.stream.closed():
            return
        try:
            self.stream.write(tornado.escape.utf8(message))
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
