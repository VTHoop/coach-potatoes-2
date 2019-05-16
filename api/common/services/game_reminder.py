from models.games.game import Game
from common.database import Database

__author__ = 'hooper-p'

Database.initialize()
Game.send_reminder()
