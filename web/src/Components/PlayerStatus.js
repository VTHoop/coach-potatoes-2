import React, { Component } from "react";
import ToggleButton from "@material-ui/lab/ToggleButton";
import ToggleButtonGroup from "@material-ui/lab/ToggleButtonGroup";
import Switch from "@material-ui/core/Switch";

class PlayerStatus extends Component {
  handleAttendanceUpdate = (event, playerStatus) => {
    this.props.player.attendance = playerStatus;
    this.props.onStatusUpdate(this.props.player);
  };

  handleBeveragesUpdate = (event, checked) => {
    this.props.player.beverages = checked;
    this.props.onStatusUpdate(this.props.player);
  };

  render() {
    const { player } = this.props;
    const playerStatus = player.attendance;

    return (
      <tr>
        <td>{player.player.number}</td>
        <td>{player.player.name}</td>
        <td className="toggleContainer">
          <ToggleButtonGroup
            value={playerStatus}
            exclusive
            onChange={this.handleAttendanceUpdate}
          >
            <ToggleButton value="Yes">Yes</ToggleButton>
            <ToggleButton value="--">--</ToggleButton>
            <ToggleButton value="No">No</ToggleButton>
          </ToggleButtonGroup>
        </td>
        <td>
          <Switch
            checked={player.beverages}
            onChange={this.handleBeveragesUpdate}
            color="primary"
          />
        </td>
      </tr>
    );
  }
}

export default PlayerStatus;
