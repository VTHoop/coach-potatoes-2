from models.attendance.attendance import Attendance
from common.database import Database

__author__ = 'hooper-p'

Database.initialize()
Attendance.update_games()