#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
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

    def _execute(self, transforms, *args, **kwargs):
        if not self.check_connection():
            return

        self.open_args = args
        self.open_kwargs = kwargs

        # EventSource only supports GET method
        if self.request.method != 'GET':
            return self.error(405, 'Method Not Allowed')
        self._write("HTTP/1.1 200 OK\r\ncontent-type: text/event-stream\r\naccess-control-allow-origin: *\r\nconnection: keep-alive\r\n\r\n")

        self.open()

    def open(self):
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

    def write_message(self, name, msg=True, wait=None):
        to_send = ""
        if wait:
            to_send += "\nretry: %s" % wait
        to_send += """\nevent: {name}\ndata: {msg}\n""".format(name=name, msg=msg)
        logging.debug(to_send)
        self._write(to_send)

    def on_connection_close(self):
        self.stream.close()
        self.close()
