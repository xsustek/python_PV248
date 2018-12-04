import urllib.request as req
from aiohttp import web
import aiohttp
import asyncio
import sys
import json


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


port = int(sys.argv[1])
host = "http://" + sys.argv[2]

session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1))


async def handleGet(request):
    heads = dict(request.headers)
    try:
        async with session.get(host + request.raw_path, headers=heads) as resp:
            res = {
                "code": resp.status,
                "headers": dict(resp.headers)
            }
            content = await resp.text()
            if is_json(content):
                res["json"] = json.loads(content)
            else:
                res["content"] = str(content)
            return web.Response(text=json.dumps(res), content_type=resp.content_type)
    except asyncio.TimeoutError:
        return web.Response(text="timeout")


async def handlePost(request):
    if is_json(await request.read()):
        js = await request.json()
        if js.__contains__("url"):
            url = js["url"]
            method = js["type"] if js.__contains__("type") else "GET"
            timeout = js["timeout"] if js.__contains__("timeout") else 1
            if method.upper() == "GET" or (method.upper() == "POST" and js.__contains__("content")): 
                content = js["content"] if js.__contains__("content") else {}
                headers = js["headers"] if js.__contains__("headers") else {}
                try:
                    async with session.request(method, url, headers=headers, timeout=timeout, data=content) as resp:
                        res = {
                        "code": resp.status,
                        "headers": dict(resp.headers)
                    }
                        content = await resp.text()
                        if is_json(content):
                            res["json"] = json.loads(content)
                        else:
                            res["content"] = str(content)
                        return web.Response(text=json.dumps(res), content_type=resp.content_type)
                except asyncio.TimeoutError:
                    return web.Response(text="timeout")
    return web.Response(text=json.dumps({"code":"invalid json"}))

app = web.Application()
app.add_routes([web.get('/{param:.*}', handleGet),
                web.post('/{params:.*}', handlePost)])

web.run_app(app, port=port)

session.close()
