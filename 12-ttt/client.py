import aiohttp
import asyncio
import sys
import json

class Game:
    def __init__(self, player, game_id):
        self.player = player
        self.game_id = game_id
        self.mark = "o" if self.player == 1 else "x"


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


def print_board(board):
    for row in board:
        for item in row:
            if item == 0: print("_", end="")
            elif item == 1: print("o", end="")
            elif item == 2: print("x", end="")
        print()


async def check_status(session, game):
    print_wait = True
    while True:
        s = dict(await status(session, game.game_id))
        if s.__contains__("next") and s["next"] != game.player:
            if print_wait:
                print_board(s["board"])
                print("waiting for the other player")
                print_wait = False
            await asyncio.sleep(1)
            continue
        if s.__contains__("winner"):
            winner = int(s["winner"])
            if winner == 0:
                print("draw")
            elif winner == game.player:
                print("you win")
            else:
                print("you lose")
            return False
        print_board(s["board"])
        return True

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def print_games(games):
    for game in games:
        print(game["id"], game["name"])

async def game(session):
    while True:
        games = await list(session)
        print_games(games)
        u_input = input()
        if u_input.startswith("new"):
            res = await new(session, "" if " " not in u_input else u_input.split(" ")[-1])
            game = Game(1, res["id"])
            break
        elif RepresentsInt(u_input):
            if any(i["id"] == int(u_input) for i in games):
                game = Game(2, int(u_input))
                break
            else:
                print("invalid input")
        else:
            print("invalid input")
    while await check_status(session, game):
        u_input = input(f"your turn ({game.mark}): ")
        if " " not in u_input:
            print("invalid input")
            continue
        u_input = u_input.split(" ")
        if not RepresentsInt(u_input[0]) or not RepresentsInt(u_input[1]):
            print("invalid input")
            continue
        x = int(u_input[0])
        y = int(u_input[-1])
        if 0 > x > 2:
            print("invalid input")
        await play(session, game.game_id, game.player, x, y)

async def main():
    async with aiohttp.ClientSession() as session:
        await game(session)

host = str(sys.argv[1])
port = int(sys.argv[2])
url = f"http://{host}:{port}"

if sys.platform == "win32":
    asyncio.set_event_loop(asyncio.ProactorEventLoop())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())