from datetime import datetime
import requests
import jinja2
import uuid

from common.database import Database
import models.games.constants as GameConstants

__author__ = 'hooper-p'




class Game(object):
    def __init__(self, date, time, venue, opponent, _id=None):
        self.date = date
        self.time = time
        self.venue = venue
        self.opponent = opponent
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "Coach Potoatoes play {} on {} at {} at {}".format(self.opponent, self.date, self.time, self.venue)

    def save_to_mongo(self):
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "date": self.date,
            "time": self.time,
            "venue": self.venue,
            "opponent": self.opponent,
            "_id": self._id
        }

    @classmethod
    def get_game_by_id(cls, _id):
        return cls(**Database.find_one(GameConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_games(cls):
        return [cls(**elem) for elem in Database.find(GameConstants.COLLECTION, {})]

    @classmethod
    def get_next_game(cls):
        games = [cls(**elem) for elem in
                 Database.find(GameConstants.COLLECTION, {})]
        for game in games:
            to_date = datetime.strptime(game.date, '%a %b %d')
            if to_date.replace(year=datetime.now().year) > datetime.now():
                return game

    @staticmethod
    def send_reminder():
        reminder_days_before_game = 11
        next_game = Game.get_next_game()
        next_game_date = datetime.strptime(next_game.date, '%a %b %d')
        next_game_date = next_game_date.replace(year=datetime.now().year)

        if (next_game_date.date() - datetime.datetime.now().date()).days == reminder_days_before_game:
            email_to = 'pat.hooper83@gmail.com'


            template = jinja2.Template(GameConstants.templateHtml)
            html = template.render(date=next_game_date, venue=next_game.venue, opponent=next_game.opponent,
                                   time=next_game.time)

            response = requests.post(GameConstants.URL,
                                     auth=('api', GameConstants.API_KEY),
                                     data={
                                         "from": GameConstants.FROM,
                                         "to": email_to,
                                         "subject": "Upcoming Game Against the {} on {}"
                                                    .format(next_game.opponent, next_game_date.strftime('%B %d')),
                                         "html": html
                                     })
            response.raise_for_status()
