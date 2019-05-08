import uuid
from bs4 import BeautifulSoup
import requests

from common.database import Database
import models.players.constants as PlayerConstants

__author__ = 'hooper-p'


class Player(object):
    def __init__(self, name, number=None, email=None, _id=None):
        self.name = name
        self.number = number
        self.email = email
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} has number {}".format(self.name, self.number)

    def save_to_mongo(self):
        Database.update(PlayerConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "name": self.name,
            "number": self.number,
            "email": self.email,
            "_id": self._id
        }

    @staticmethod
    def update_players():
        link = "https://www.hnir.net/roster/show/4943794?subseason=602048"
        request = requests.get(link)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")

        roster = soup.find("tbody", {"id": "rosterListingTableBodyPlayer"})

        roster_rows = roster.find_all("tr")

        for rr in roster_rows:
            player_info = rr.find_all("td")
            name = player_info[1].a.text.strip()
            number = player_info[0].text.strip()
            Player(name, number).save_to_mongo()

        for pta in PlayerConstants.players_to_add:
            Player(pta['name'], pta['number'], pta['email']).save_to_mongo()


    @classmethod
    def get_player_by_id(cls, _id):
        return cls(**Database.find_one(PlayerConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_players(cls):
        return [cls(**elem) for elem in Database.find(PlayerConstants.COLLECTION, {})]