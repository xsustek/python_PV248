import aiohttp
import asyncio
import sys
import json

async def list(session):
    async with session.get(f"{url}/list") as resp:
        res = await resp.text()
        return json.loads(res)

async def status(session, id):
    async with session.get(f"{url}/status?game={id}") as resp:
        res = await resp.text()
        return json.loads(res)

async def new(session, name):
    async with session.get(f"{url}/start?name={name}") as resp:
        res = await resp.text()
        return json.loads(res)

async def play(session, game, player, x, y):
    async with session.get(f"{url}/play?game={game}&player={player}&x={x}&y={y}") as resp:
        res = await resp.text()
        return json.loads(res)

async def game(session):
    while True:
        input()
        print(await list(session))

async def main():
    async with aiohttp.ClientSession() as session:
        await game(session)

host = str(sys.argv[1])
port = int(sys.argv[2])
url = f"http://{host}:port"

if sys.platform == "win32":
    asyncio.set_event_loop(asyncio.ProactorEventLoop())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())