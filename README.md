tornado-eventsource
===================

[![Dependency Status](https://gemnasium.com/guilhermef/tornado-eventsource.svg)](https://gemnasium.com/guilhermef/tornado-eventsource)
[![Build Status](https://travis-ci.org/guilhermef/tornado-eventsource.svg?branch=master)](https://travis-ci.org/guilhermef/tornado-eventsource)

A simple EventSource handler for tornado.
With a built-in client for testing.

[EventSource on MDN](https://developer.mozilla.org/en-US/docs/Server-sent_events/Using_server-sent_events)

How to use
----------

Install it(duh!):

    pip install tornado_eventsource

On your handler:

    class MyAmazingHandler(EventSourceHandler):
        def check_connection(self):
            if youDontFitMyCondition:
                self.error(403, 'forbidden')
                return False
            return True

        def open(self):
            self.write_message('doge_source', 'much connection')

        def close(self):
            # Cleanup after close

[<img src="http://cdn.meme.am/instances/500x/57038109.jpg">](https://developer.mozilla.org/en-US/docs/Server-sent_events/Using_server-sent_events)

Using the client for test:

    from tornado_eventsource.event_source_client import eventsource_connect

    ...
    
    def test_get_message_on_open(self):
        event_source = eventsource_connect(url=self.get_url('/'), callback=self.stop)
        self.wait()
        event = event_source.result().events[0]
        self.assertEqual(event.name, 'doge_source')
        self.assertEqual(event.data, 'much connection')

Contribute
----------

    make setup

    change things

    make test

    pull request ;)

License
-------

> The MIT License (MIT)
>
> Copyright (c) 2014 Guilherme Souza, A.k.a.: Galinho
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
