import React, { Component } from "react";
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';

class GameRow extends Component {
  handleClickOpen = () => {
    this.props.onRowClick(this.props.value);
  };

  render() {
    return (
      <TableRow
        className="stripe-green grow"
        onClick={this.handleClickOpen}
      >
        <TableCell className="pa3">{this.props.value.date}</TableCell>
        <TableCell className="pa3">{this.props.value.time}</TableCell>
        <TableCell className="pa3">{this.props.value.venue}</TableCell>
        <TableCell className="pa3">{this.props.value.opponent}</TableCell>
      </TableRow>
    );
  }
}

export default GameRow;
