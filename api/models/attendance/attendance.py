from bs4 import BeautifulSoup
import requests

from common.database import Database
from models.games.game import Game
from models.players.player import Player

import models.players.constants as PlayerConstants

__author__ = 'hooper-p'

import uuid

import models.attendance.constants as AttendanceConstants


class Attendance(object):
    def __init__(self, game, player, attendance='--', beverages=False, _id=None):
        self.game = Game.get_game_by_id(game)
        self.player = Player.get_player_by_id(player['_id'])
        self.attendance = attendance
        self.beverages = beverages
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} says {} to game on {}".format(self.player.name, self.attendance, self.game.date)

    def save_to_mongo(self):
        Database.update(AttendanceConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "game": self.game._id,
            "player": self.player.json(),
            "attendance": self.attendance,
            "beverages": self.beverages,
            "_id": self._id
        }

    @classmethod
    def get_all_attendance(cls):
        return [cls(**elem) for elem in Database.find(AttendanceConstants.COLLECTION, {})]

    @classmethod
    def get_attendance_by_game(cls, game):
        all_players = [cls(**elem) for elem in Database.find_and_sort(AttendanceConstants.COLLECTION, {"game": game},
                                                                      [("attendance", -1), ("player.number", 1),
                                                                       ("player.name", 1)])]
        for player in all_players[:]:
            if player.player.name in PlayerConstants.players_to_remove:
                all_players.remove(player)
        return all_players

    @classmethod
    def yes_attendance_by_game(cls, game):
        return [cls(**elem) for elem in
                Database.find(AttendanceConstants.COLLECTION, {"game": game, "attendance": "Yes"})]

    @classmethod
    def get_attendance_by_id(cls, attendance_id):
        return cls(**Database.find_one(AttendanceConstants.COLLECTION, {"_id": attendance_id}))

    @staticmethod
    def build_first():
        players = Player.get_players()
        games = Game.get_games()
        for game in games:
            for player in players:
                Attendance(game._id, player.json()).save_to_mongo()

    @staticmethod
    def build_for_new_game(game):
        players = Player.get_players()
        game = Game.get_game_by_id(game)
        for player in players:
            Attendance(game._id, player.json()).save_to_mongo()

    @staticmethod
    def update_games():
        # this is used to find the id within the href of the time element on the schedule
        find_str = 'games'

        link = "https://www.hnir.net/schedule/team_instance/4588311?subseason=602048"
        request = requests.get(link)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")

        schedule = soup.find("tbody")

        schedule_rows = schedule.find_all("tr", {"class": "compactGameList"})

        for sr in schedule_rows:
            game_info = sr.find_all("td")
            date = game_info[1].text.strip()
            opponent = game_info[3].a.text.strip()
            time = game_info[5].a.text.strip()
            venue = game_info[4].text.strip()
            id = game_info[0].text

            # 8 digit number after "games/" is used as id for game
            # slice_id = id[id.find(find_str) + 6:id.find(find_str) + 14]

            game = Database.find_one('games', {"_id": id})
            if game is None:
                new_game = Game(date, time, venue, opponent, id)
                new_game.save_to_mongo()
                Attendance.build_for_new_game(new_game._id)
            else:
                game = Game.get_game_by_id(id)
                game.date = date
                game.opponent = opponent
                game.time = time
                game.venue = venue
                game.save_to_mongo()
