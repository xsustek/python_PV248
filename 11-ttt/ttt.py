import urllib.request as req
from aiohttp import web
import aiohttp
import asyncio
import sys
import json
import os


class Games:
    def __init__(self, *args, **kwargs):
        self.games = {}
        self.current_id = 1

    def get_id(self):
        id = self.current_id
        self.current_id += 1
        return id

    def start_new_game(self, name):
        id = self.get_id()
        game = Game(name, id)
        self.games[id] = game
        return game

    def game_list(self):
        return self.games.values()


class Game:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.winner = 0
        self.over = False
        self.next = 1

    def play(self, player, x, y):
        if player != self.next:
            return {"status": "bad", "message": f"next shoud be player {self.next}"}
        if self.over:
            return {"status": "bad", "message": "game is over"}
        if self.board[x][y] != 0:
            return {"status": "bad", "message": "field is alredy filled"}
        self.board[x][y] = player
        self.set_next()
        self.check_game_status()
        return {"status": "ok"}

    def set_next(self):
        if self.next == 1:
            self.next = 2
        else:
            self.next = 1

    def check_game_status(self):
        for row in self.board:
            if(all(0 != row[0] == item for item in row)):
                self.winner = row[0]
                self.over = True
                return
        for i in range(3):
            if 0 != self.board[0][i] == self.board[1][i] == self.board[2][i]:
                self.winner = self.board[0][i]
                self.over = True
                return
        if 0 != self.board[0][0] == self.board[1][1] == self.board[2][2]:
            self.winner = self.board[0][0]
            self.over = True
            return
        if 0 != self.board[0][2] == self.board[1][1] == self.board[2][0]:
            self.winner = self.board[0][2]
            self.over = True
            return
        if all(0 != item for item in row for row in self.board):
            self.over = True
            return


    def result(self):
        if self.over:
            return {"winner": self.winner}
        return {"board": self.board, "next": self.next}


async def start(params: web.Request):
    name = params.rel_url.query["name"]
    game = games.start_new_game(name)
    return web.json_response({"id": game.id})


async def status(params: web.Request):
    game = int(params.rel_url.query["game"])
    return web.json_response(games.games[game].result())


async def play(params: web.Request):
    game = int(params.rel_url.query["game"])
    player = int(params.rel_url.query["player"])
    x = int(params.rel_url.query["x"])
    y = int(params.rel_url.query["y"])
    res = games.games[game].play(player, x, y)
    return web.json_response(res)

async def list(params):
    res = [{"id": game.id, "name": game.name} for game in games.game_list()]
    return web.json_response(res)

games = Games()
port = int(sys.argv[1])
app = web.Application()
app.add_routes([web.get('/start{params:.*}', start),
                web.get('/status{params:.*}', status),
                web.get('/play{params:.*}', play),
                web.get('/list{params:.*}', list)])

web.run_app(app, port=int(port))
