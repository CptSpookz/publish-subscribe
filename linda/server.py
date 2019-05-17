import asyncio
import socket
import json

from sys import exit
from collections import deque

from linda.utils import pack, unpack

tuples = {}


class LindaServer(asyncio.Protocol):
    def connection_made(self, transport):
        self._transport = transport
        self._buffer = bytes()
        self._expected_size = -1

    def connection_lost(self, exc):
        if not exc:
            print('Connection has been closed.')
        else:
            print('Error: ' + repr(exc))

    def data_received(self, data):
        while len(data) > 0:
            if self._expected_size < 0:
                if len(data.split(b':', 1)) == 2:
                    size, data = data.split(b':', 1)
                    try:
                        self._expected_size = int(size)
                    except ValueError:
                        self._transport.close()
            self._buffer = data[:self._expected_size]
            if self._expected_size > 0 and len(data) >= self._expected_size:
                data = data[self._expected_size:]
                self._expected_size = -1
                self._call(unpack(self._buffer.decode('utf-8')))
                self._buffer = bytes()

    def _call(self, message):
        if message['op'] == 'out':
            self._out(message)
        elif message['op'] == 'rd':
            self._rd(message)
        elif message['op'] == 'in':
            self._in(message)

    def _out(self, message):
        sender = message['sender']
        topic = message['topic']
        content = message['msg']

        topic_tuple = self._get_topic(sender, topic)
        topic_tuple['messages'].append(content)
        self._wait_iteration(topic_tuple)

    def _rd(self, message):
        sender = message['sender']
        topic = message['topic']

        topic_tuple = self._get_topic(sender, topic)
        self._register_connection(topic_tuple, message)
        self._wait_iteration(topic_tuple)

    def _in(self, message):
        sender = message['sender']
        topic = message['topic']
        topic_tuple = self._get_topic(sender, topic)
        self._register_connection(topic_tuple, message)
        self._wait_iteration(topic_tuple)

    def _get_topic(self, sender, topic):
        global tuples
        sender_tuple = tuples.get(sender)
        
        if not sender_tuple:
            sender_tuple = tuples[sender] = {}

        topic_tuple = sender_tuple.get(topic)
        if not topic_tuple:
            topic_tuple = sender_tuple[topic] = {'messages': deque(), 'subscribers': deque()}

        return topic_tuple

    def _register_connection(self, topic_tuple, message):
        topic_tuple['subscribers'].append((message, self._transport))

    def _wait_iteration(self, topic_tuple):
        messages = topic_tuple['messages']
        subscribers = topic_tuple['subscribers']

        while len(messages) > 0 and len(subscribers) > 0:
            message, conn = subscribers.popleft()
            message['msg'] = messages[0]
            conn.write(pack(message))
            if message['op'] == 'in':
                messages.popleft()


async def start_server(port=15555):
    try:
        loop = asyncio.get_running_loop()
        print(f'Starting socket server on localhost:{port}')
        server = await loop.create_server(lambda: LindaServer(), 'localhost', port)
    
        async with server:
            await server.serve_forever()
    
    except RuntimeError as re:
        print('Error: ' + re)

