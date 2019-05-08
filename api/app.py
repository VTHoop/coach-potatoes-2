from models.attendance.attendance import Attendance
from models.players.player import Player

__author__ = 'hooper-p'

from flask import Flask, jsonify
from flask_cors import CORS
from common.database import Database

from models.games.game import Game

from models.attendance.views import attendance_blueprint

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = '123'

app.register_blueprint(attendance_blueprint, url_prefix='/attendance')

CORS(app)

@app.before_first_request
def init_db():
    Database.initialize()
    Player.update_players()
 

@app.route('/', methods=['GET', 'OPTIONS'])
def home():
    Attendance.update_games()
    # Attendance.build_first()
    # return render_template('base.html')
    games = Game.get_games()
    games_json = [game.json() for game in games]
    for a in Attendance.get_all_attendance():
        a.save_to_mongo()

    return jsonify(games_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4990)

