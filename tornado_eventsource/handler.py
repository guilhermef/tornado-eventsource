#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import asyncio

import tornado.web
import tornado.gen as gen
from tornado import httputil
from tornado.iostream import StreamClosedError
import logging


class EventSourceHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
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
            "Connection": "keep-alive",
            "Date": httputil.format_timestamp(time.time()),
        }
        default_headers.update(self.custom_headers())
        self._headers = httputil.HTTPHeaders(default_headers)

    async def wait_for_stream_close(self):
        while not self.stream.closed():
            await asyncio.sleep(10)

    async def get(self, *args, **kwargs):
        self.check_connection()

        self.open(*args, **kwargs)

        await self.wait_for_stream_close()

    def open(self, *args, **kwargs):
        pass

    def close(self):
        pass

    def _write(self, message):
        if self.stream.closed():
            return
        try:
            self.write(message)
            return self.flush()
        except StreamClosedError:
            logging.exception('Stream Closed')
            self.close()

    def write_message(self, name=None, msg=True, wait=None, evt_id=None):
        to_send = ""
        if wait:
            to_send += f"\nretry: {wait}"
        if name:
            to_send += f"""\nevent: {name}"""
        if evt_id:
            to_send += f"""\nid: {evt_id}"""
            for line in msg.splitlines(False):
                to_send += f"""\ndata: {line}"""
        else:
            to_send += f"""\ndata: {msg}"""
        to_send += "\n\n"
        logging.debug(to_send)
        return self._write(to_send)

    def on_connection_close(self):
        self.stream.close()
        self.close()
