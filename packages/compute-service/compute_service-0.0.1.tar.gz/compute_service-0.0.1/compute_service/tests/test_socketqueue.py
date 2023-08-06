import asyncio
import os

from compute_service.queue.socketqueue import UnixSocketQueue


def test_socketqueue(tmp_path):
    sock = tmp_path / "tmp.sock"

    async def do_test():
        query = UnixSocketQueue(socket_path=sock)
        server_task = asyncio.create_task(query.start_server())
        await asyncio.sleep(0.5)

        data1 = bytearray(os.urandom(1000000))
        data2 = b'tests'

        await query.submit(data1)
        await query.submit(data2)

        res1 = await query.get()
        res2 = await query.get()

        assert data1 == res1
        assert data2 == res2

        server_task.cancel()

    asyncio.run(do_test())
