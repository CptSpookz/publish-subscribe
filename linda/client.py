import asyncio
import socket
import json

from .utils import pack, unpack


class LindaClient():
    def __init__(self, host='localhost', port=15555):
        self._reader = None
        self._writer = None
        self.host = host
        self.port = port

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()

    async def _recvall(self):
        buf = b''
        size = -1

        while True:
            data = await self._reader.read(1024)
            try:
                if len(data.split(b':', 1)) == 2:
                    size, data = data.split(b':', 1)
                    size = int(size)

                else:
                    buf += data
                    data = b''

            except Exception as e:
                print('Error: ' + e)
            
            if size > 0 and len(data) >= size:
                return data

    def _out(self, data):
        message = pack({'op': 'out', 'sender': data[0], 'topic': data[1], 'msg': data[2]})
        self._writer.write(message)
   
    async def _rd(self, data):
        message = pack({'op': 'rd', 'sender': data[0], 'topic': data[1]})
        self._writer.write(message)
        
        response = await self._recvall()
        response = unpack(response)
        return self._cast(data[2], response)

    async def _in(self, data):
        message = pack({'op': 'in', 'sender': data[0], 'topic': data[1]})
        self._writer.write(message)
        
        response = await self._recvall()
        response = unpack(response)
        return self._cast(data[2], response)

    def _cast(self, cast, msg):
        if type(cast) is type:
            return cast(msg)
        else:
            return msg


