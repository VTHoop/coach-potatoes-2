import os

__author__ = 'hooper-p'

COLLECTION = 'games'
ATTENDANCE_COLLECTION = 'attendance'
URL = os.environ.get("MAILGUN_URL")
API_KEY = os.environ.get("MAILGUN_API")