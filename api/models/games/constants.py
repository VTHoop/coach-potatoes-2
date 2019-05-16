import os

__author__ = 'hooper-p'

COLLECTION = 'games'
ATTENDANCE_COLLECTION = 'attendance'
URL = os.environ.get("MAILGUN_URL")
API_KEY = os.environ.get("MAILGUN_API")
FROM = 'Taters <postmaster@richmondcoachpotatoes.club>'
templateHtml = '<h3>Taaaaters!  We have an upcoming game on {{ date.strftime("%B %d")  | replace(" 0", " ") }} ' \
                '@ {{time}} against the {{ opponent }} at {{ venue }}</h3>' \
               '<br><p>Who\'s in?  Either Reply All or go to the site to let everyone know.' \
               '<br><p><a href="richmondcoachpotatoes.club">richmondcoachpotatoes.club</a>'
