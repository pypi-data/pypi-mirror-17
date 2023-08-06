#!/usr/bin/env python
import argparse
import asyncio
import hashlib
import itertools
import logging
import os
import time
import urllib.parse
from collections import OrderedDict, deque

import websockets
from websockets.protocol import OPEN

from wsstat.gui import build_urwid_loop, Logger, BlinkBoard

logging.basicConfig(level=logging.FATAL)

class ConnectedWebsocketConnection(object):
    def __init__(self, ws, token):
        self.ws = ws
        self.api_token = token
        self.id = self.api_token[:8]
        self._message_count = itertools.count()
        self.last_message_recv = 0
        self.started = time.time()

    @property
    def message_count(self):
        return int(repr(self._message_count)[6:-1])

    def increment_message_counter(self):
        next(self._message_count)

    def __repr__(self):
        return "<Websocket {}>".format(self.id)

class WebsocketTestingClient(object):
    def __init__(self, websocket_url, total_connections, max_connecting_sockets=5):
        # Configuration stuff
        self.frame = None
        self.websocket_url = urllib.parse.urlparse(websocket_url)
        self.total_connections = total_connections

        # Asyncio stuff
        self.loop = asyncio.get_event_loop()
        self.connection_semaphore = asyncio.Semaphore(max_connecting_sockets)

        # Counts and buffers
        self.global_message_counter = itertools.count()
        self.sockets = OrderedDict()
        self.ring_buffer = deque(maxlen=10)

        self.setup_tasks()

        self.blinkboard = BlinkBoard()
        self.logger = Logger()
        self.widgets = [
            self.blinkboard.widget,
            (10, self.logger.widget)
        ]

    @property
    def messages_per_second(self):
        return self._get_current_messages_per_second()

    @asyncio.coroutine
    def create_websocket_connection(self):
        # Generate a random API token
        api_token = hashlib.sha256(os.urandom(4)).hexdigest()

        # Make len(connection_semaphore) connection attempts at a time
        with (yield from self.connection_semaphore):
            # Signify that this socket is connecting
            self.sockets[api_token[:8]] = None

            # Await the connection to complete successfully
            websocket = yield from websockets.connect(self.websocket_url.geturl(), extra_headers={"x-endpoint-token": api_token})

            # Create our handler object
            connected_websocket = ConnectedWebsocketConnection(websocket, api_token)

            # Update the connected_sockets table
            self.sockets[connected_websocket.id] = connected_websocket

            # Log that we connected successfully
            self.logger.log("[{}] Connected!".format(connected_websocket.id))

        try:
            # Just loop and recv messages
            while True:
                # import random
                # if random.random() < .5:
                #     await websocket.send("DERP")

                # Wait for a new message
                yield from websocket.recv()

                # Test random disconnects
                # import random
                # if random.random() < 0.01:
                #     await connected_websocket.ws.close(reason="Peace out homie!")

                # Increment our counters
                next(self.global_message_counter)

                connected_websocket.increment_message_counter()

                connected_websocket.last_message_recv = time.time()

        except Exception as e:
            # Log the exception
            self.logger.log("[{}] {}".format(connected_websocket.id, e))

    @asyncio.coroutine
    def update_urwid(self):
        interval = .1
        status_line = "{hostname} | Connections: [{current}/{total}] | Total Messages: {message_count} | Messages/Second: {msgs_per_second}/s"

        while True:
            # Only update things a max of 10 times/second
            yield from asyncio.sleep(interval)

            # Get the current global message count
            global_message_count = int(repr(self.global_message_counter)[6:-1])
            self.ring_buffer.append(global_message_count)

            currently_connected_sockets = len([x for x in self.sockets.values() if x and x.ws.state == OPEN])

            self.logger.update_graph_data([self.messages_per_second,])

            # Get and update our blinkboard widget
            self.blinkboard.generate_blinkers(self.sockets)
            # Make the status message
            status_message = status_line.format(
                hostname=self.websocket_url.netloc,
                current=currently_connected_sockets,
                total=self.total_connections,
                message_count=global_message_count,
                msgs_per_second=self.messages_per_second
            )
            self.frame.footer.set_text(status_message)

    def setup_tasks(self):
        coroutines = []
        for _ in range(self.total_connections):
            coroutines.append(self.loop.create_task(self.create_websocket_connection()))

        coroutines.append(self.update_urwid())

        # Gather all the tasks needed
        self.tasks = asyncio.gather(*coroutines)

        # Schedule the tasks
        asyncio.ensure_future(self.tasks)

    def exit(self):
        for task in asyncio.Task.all_tasks(self.loop):
            task.cancel()
        self.loop.stop()
        return True

    def unhandled_input(self, keypress):
        if keypress == "q":
            self.exit()
        return True

    def _get_current_messages_per_second(self):
        # Calculate deltas over the past window
        deltas = [y - x for x, y in zip(list(self.ring_buffer), list(self.ring_buffer)[1:])]

        # If the deque isn't empty
        if deltas:
            msgs_per_second = '{0:.2f}'.format(float(sum(deltas) / len(self.ring_buffer)) * 10)
        else:
            msgs_per_second = '{0:.2f}'.format(float(0.0))

        return msgs_per_second


def run():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("websocket_url", help="The websocket URL to hit")
    parser.add_argument("-n", "--num-clients", help="Number of clients to connect - default 250", action="store",
                        default="250", type=int)
    parser.add_argument("-c", "--max-connects", help="Number of connections to simultaniously open - default 15",
                        action="store", default="15", type=int)
    args = parser.parse_args()

    # Spin up a client
    client = WebsocketTestingClient(args.websocket_url, total_connections=args.num_clients,
                                    max_connecting_sockets=args.max_connects)

    # Get the urwid loop
    urwid_loop = build_urwid_loop(client)

    urwid_loop.run()

    client.loop.close()

if __name__ == "__main__":
    run()