import uuid

import tornado.ioloop
import tornado.web
import tornado_eventsource.handler


class MainHandler(tornado_eventsource.handler.EventSourceHandler):
    def open(self):
        ioloop = tornado.ioloop.IOLoop.instance()
        self.heart_beat = tornado.ioloop.PeriodicCallback(self._simple_callback, 5000, ioloop)
        self.heart_beat.start()

    def _simple_callback(self):
        self.write_message(name="doge", msg="Wow much alive\nSuch message", evt_id=uuid.uuid4())
        self.write_message(msg="Wow much nameless", id=uuid.uuid4())

application = tornado.web.Application([
    (r"/", MainHandler),
], debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
