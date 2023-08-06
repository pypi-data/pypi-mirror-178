import asyncio
import os
from collections import deque


async def _write_and_eof(writer, data):
    if data is not None:
        writer.write(data)
    writer.write_eof()
    await writer.drain()


async def _read_all(reader):
    buf = []
    while True:
        line = await reader.readline()
        if not line:
            break

        buf.append(line)

    return b''.join(buf)


class UnixSocketQueue():
    def __init__(self, socket_path='/tmp/compute_local_queue.sock'):
        self._socket_path = socket_path
        self._queue = deque()


    async def start_server(self):
        if os.path.exists(self._socket_path):
            raise ValueError(f'Socket already exits: {self._socket_path}')

        server = await asyncio.start_unix_server(self._handle_client, path=self._socket_path)

        print(f'UnixSocketQueue serving on "{self._socket_path}"')

        try:
            async with server:
                await server.serve_forever()
        finally:
            os.remove(self._socket_path)


    async def _handle_client(self, reader, writer):
        data = await reader.read(100)

        if data.startswith(b'SUBMIT '):
            rest_data = await _read_all(reader)
            self._queue.append(data[7:] + rest_data)
            await _write_and_eof(writer, b'OK')
        elif data == b'GET':
            if not self._queue:
                await _write_and_eof(writer, None)
            else:
                data = self._queue.popleft()
                await _write_and_eof(writer, data)
        else:
            await _write_and_eof(writer, None)

        writer.close()


    async def submit(self, data):
        reader, writer = await asyncio.open_unix_connection(path=self._socket_path)
        await _write_and_eof(writer, b'SUBMIT ' + data)
        response = await _read_all(reader)
        if response != b'OK':
            raise ValueError(f'Invalid server response: {response}')

        writer.close()

    
    async def get(self):
        reader, writer = await asyncio.open_unix_connection(path=self._socket_path)
        await _write_and_eof(writer, b'GET')
        data = await _read_all(reader)
        writer.close()
        if data == b'':
            return None

        return data
