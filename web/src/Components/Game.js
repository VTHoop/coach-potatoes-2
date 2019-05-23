import React, {Component} from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";

import "./Game.css";
import PlayerStatus from "./PlayerStatus";



class AttendanceDialog extends Component {

  handleUpdate = (player) => {
    var foundIndex = this.props.attendance.findIndex(oldPlayer => oldPlayer._id === player._id);
    this.props.attendance[foundIndex] = player;
    this.props.updateAttendance(this.props.attendance);
  };

  render() {
    return (
      <div>
        <Dialog
          fullWidth={true}
          open={this.props.gameDialogStatus}
          onClose={this.props.onClose}
          aria-labelledby="form-dialog-title"
        >
          <DialogTitle id="form-dialog-title">Game Attendance</DialogTitle>
          <DialogContent>
          <div className="w-100 tc yes_number"><strong>{this.props.how_many}</strong> people say they're coming this game.</div>

            <table className="f6 w-100 mw8 center">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Status</th>
                  <th>Beers?</th>
                </tr>
              </thead>
              <tbody>
                {this.props.attendance.map(player => (
                  <PlayerStatus
                    key={player._id}
                    player={player}
                    onStatusUpdate={this.handleUpdate}
                  />
                ))}
              </tbody>
            </table>

          </DialogContent>
          <DialogActions>
            <Button onClick={this.props.onClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.props.onSave} color="primary">
              Save
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

export default AttendanceDialog;
