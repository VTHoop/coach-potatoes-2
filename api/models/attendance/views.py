from flask import Blueprint, render_template, request, jsonify

from models.attendance.attendance import Attendance

__author__ = 'hooper-p'

attendance_blueprint = Blueprint('attendance', __name__)


@attendance_blueprint.route('/<string:game_id>', methods=['GET', 'POST', 'PUT'])
def view_game(game_id):

    if request.method == 'PUT':
        # loop over request.json
        # find database object relating to id
        # update object with json
        players = Attendance.get_attendance_by_game(game_id)
        for a in request.json:
            player = next((x for x in players if x._id == a['_id']), None)
            if player:
                player.attendance = a['attendance']
                player.beverages = a['beverages']
                player.save_to_mongo()

    players = Attendance.get_attendance_by_game(game_id)
    # how_many = Attendance.yes_attendance_by_game(game_id)
    attendance_json = [player.json() for player in players]
    return jsonify(attendance_json)

    # return render_template("attendance/game_attendance.html", attendance=attendance, how_many=len(how_many))
