import urllib.request as req
from aiohttp import web
import aiohttp
import asyncio
import sys
import json
import os

port = int(sys.argv[1])
dir = str(sys.argv[2])

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(
    loop=loop, timeout=aiohttp.ClientTimeout(total=1))


def read_file(file_name):
    with open(file_name, mode="r") as f:
        return f.read()


async def handleGet(request):
    file_name = request.match_info['params']  # Could be a HUGE file
    headers = {
        "Content-disposition": "attachment; filename={file_name}".format(file_name=file_name)
    }

    file_path = os.path.join(dir, file_name)

    if not os.path.exists(file_path):
        return web.Response(
            body='File <{file_name}> does not exist'.format(
                file_name=file_name),
            status=404
        )

    if not os.path.isfile(file_path):
        return web.Response(status=403)

    return web.Response(
        body=read_file(file_path),
        headers=headers
    )


async def handlePost(request):
    pass


app = web.Application()
app.add_routes([web.get('/{params:.*}', handleGet),
                web.post('/{params:.*}', handlePost)])

web.run_app(app, port=int(port))

session.close()

loop.close()
