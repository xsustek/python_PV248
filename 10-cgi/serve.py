import urllib.request as req
from aiohttp import web
import aiohttp
import asyncio
import sys
import json
import os

port = int(sys.argv[1])
dir = str(sys.argv[2])


def set_variables(request, script_name):
    for header_key, header_val in request.headers.items():
        os.putenv("HTTP_" + header_key.upper().replace('-', '_'), header_val)

    os.putenv("CONTENT_TYPE",
              request.content_type if request.content_type is not None else "")
    os.putenv("CONTENT_LENGTH", str(request.content_length)
              if request.content_length is not None else "")
    os.putenv('GATEWAY_INTERFACE', 'CGI/1.1')
    os.putenv('PATH_INFO', request.match_info['params'])
    os.putenv('QUERY_STRING', request.query_string)
    os.putenv('REMOTE_ADDR', '127.0.0.1')
    os.putenv('REQUEST_METHOD', request.method)
    os.putenv('SCRIPT_NAME', script_name)
    os.putenv('SERVER_NAME', '127.0.0.1')
    os.putenv('SERVER_PORT', str(port))
    os.putenv('SERVER_PROTOCOL', 'HTTP/1.1')
    os.putenv('SERVER_SOFTWARE', 'PV248/1')
    os.putenv('REMOTE_HOST', 'NULL')


async def start_cgi(file_path, program_data):
    process = await asyncio.create_subprocess_shell(file_path, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
    return (await process.communicate(program_data if program_data is not None else b''))[0]


async def handle_request(request):
    file_name = request.match_info['path'] + '.cgi'

    file_path = os.path.join(dir, file_name)

    if not os.path.exists(file_path):
        return web.Response(
            body='404: Not Found',
            status=404
        )

    content = None
    if request.method == 'POST':
        content = await request.read()

    set_variables(request, file_name)
    cgi_res = await start_cgi(file_path, content)
    return web.Response(text=cgi_res.decode('utf-8'))


if sys.platform == "win32":
    asyncio.set_event_loop(asyncio.ProactorEventLoop())

app = web.Application()
app.add_routes([web.get('/{path:.*}.cgi{params:.*}', handle_request),
                web.post('/{path:.*}.cgi{params:.*}', handle_request),
                web.static('/', path=dir)])

web.run_app(app, port=int(port))
