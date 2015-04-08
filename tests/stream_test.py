#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tests import EventSourceTestCase
from tornado_eventsource.event_source_client import eventsource_connect
from tornado.iostream import StreamClosedError

from mock import patch


class PostMessageTest(EventSourceTestCase):

    def test_returns_405_if_post(self):
        response = self.fetch('/', method='POST', body='a')
        self.assertEqual(response.code, 405)

    def test_returns_405_if_put(self):
        response = self.fetch('/', method='PUT', body='a')
        self.assertEqual(response.code, 405)

    @patch('tornado.iostream.IOStream.write')
    def test_stream_closed_error(self, write_mock):
        write_mock.side_effect = StreamClosedError
        event_source = eventsource_connect(url=self.get_url('/'), callback=self.stop)
        self.wait()
        self.assertRaises(Exception, event_source.result)

    def test_check_connection_error(self):
        response = self.fetch('/forbidden', method='GET')
        self.assertEqual(response.code, 403)

    def test_should_set_custom_headers(self):
        event_source = eventsource_connect(url=self.get_url('/'), callback=self.stop)
        self.wait()
        headers = event_source.result().headers

        self.assertEqual(headers['Transfer-Encoding'], 'identity')
        self.assertEqual(headers['Connection'], 'keep-alive')
        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertEqual(headers['Content-Type'], 'text/event-stream')
        self.assertEqual(headers['X-doge-header'], 'much head')

    def test_get_message_on_open(self):
        event_source = eventsource_connect(url=self.get_url('/'), callback=self.stop)
        self.wait()
        event = event_source.result().events[0]
        self.assertEqual(event.name, 'doge_source')
        self.assertEqual(event.data, 'much connection')

    def test_get_message_with_retry_on_open(self):
        event_source = eventsource_connect(url=self.get_url('/retry'), callback=self.stop)
        self.wait()
        event = event_source.result().events[0]
        self.assertEqual(event.name, 'doge_source')
        self.assertEqual(event.data, 'such Wow')
        self.assertEqual(event.retry, 300)

    def test_get_message_with_url_params(self):
        event_source = eventsource_connect(url=self.get_url('/param/42'), callback=self.stop)
        self.wait()
        event = event_source.result().events[0]
        self.assertEqual(event.name, 'doge_source')
        self.assertEqual(event.data, 'such Wow 42')

    def test_get_message_without_name(self):
        event_source = eventsource_connect(url=self.get_url('/no_name'), callback=self.stop)
        self.wait()
        event = event_source.result().events[0]
        self.assertEqual(event.name, None)
        self.assertEqual(event.data, 'such Wow')

    def test_get_message_with_multiline(self):
        event_source = eventsource_connect(url=self.get_url('/multi_line'), callback=self.stop)
        self.wait()
        event = event_source.result().events[0]
        self.assertEqual(event.name, None)
        self.assertEqual(event.data, 'such Wow\nmuch multi')
