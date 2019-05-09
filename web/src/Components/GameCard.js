import React, { Component } from "react";
import "./GameCard.css";
import "../App.css";
import AttendanceDialog from "./Game";
import GameRow from "./GameRow";
import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';

import axios from "axios";

export default class GameCard extends Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      games: [],
      attendance: [],
      gameDialogActive: false,
      currentGame: '',
    };
  }
  apiBase = "http://68.183.30.13:4990";
  attendanceRoute = "attendance";

  componentDidMount() {
    axios.get(`${this.apiBase}/`).then(res => {
      const games = res.data;
      const sortedGames = this.completeToBottom(games);
      this.setState({ games: sortedGames });
    });
  }

  onAttendanceUpdate = (attendance) => {
    this.setState({ attendance });
  };


  onRowClick = game => {
    this.setState({ gameDialogActive: true });
    this.setState({ currentGame: game });
    axios
      .get(`${this.apiBase}/${this.attendanceRoute}/${game._id}`)
      .then(res => {
        const attendance = res.data;
        attendance.sort(this.compareNums);
        attendance.sort(this.yesNoSort);
        this.setState({ attendance });
      });
  };

  handleClose = () => {
    this.setState({ gameDialogActive: false });
  };

  handleSave = () => {
    axios.put(`${this.apiBase}/${this.attendanceRoute}/${this.state.currentGame._id}`, this.state.attendance)
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
    this.setState({ gameDialogActive: false });
  }

  completeToBottom = (games) => {
    let final = []; 
    const completeGames = games.filter(game => game.time === 'Complete');
    const openGames = games.filter(game => game.time !== 'Complete');
    openGames.map(game => final.push(game));
    completeGames.map(game => final.push(game));
    return final; 
  }

  compareNums = (a, b) => {
    if (Number(a.player.number) < Number(b.player.number)) return -1;
    if (Number(a.player.number) > Number(b.player.number)) return 1;
    return 0;
  };

  yesNoSort = (a, b) => {
    var x = a.attendance.toLowerCase();
    var y = b.attendance.toLowerCase();
    return ((x < y) ? 1 : ((x > y) ? -1 : 0));
  }

  render() {
    return (
      <>
      <div className="f6 w-100 mw8 center">
          <img
            alt="team_logo"
            className="logo center"
            src={require("../logo.png")}
          />
        </div>
        <div className="pa4">
          <div className="overflow-auto">
            <Table className="f6 w-100 mw8 center" cellSpacing="0">
              <TableHead>
                <TableRow className="stripe-dark">
                  <TableCell className="table-header pa3 bg-white">Date</TableCell>
                  <TableCell className="table-header tl pa3 bg-white">Time</TableCell>
                  <TableCell className="table-header tl pa3 bg-white">Location</TableCell>
                  <TableCell className="table-header tl pa3 bg-white">Opponent</TableCell>
                </TableRow>
              </TableHead>
              <TableBody className="lh-copy">
                {this.state.games.map(game => (
                  <GameRow
                    key={game._id}
                    value={game}
                    onRowClick={this.onRowClick}
                  />
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
        <AttendanceDialog
          gameDialogStatus={this.state.gameDialogActive}
          attendance={this.state.attendance}
          onClose={this.handleClose}
          onSave={this.handleSave}
          updateAttendance={this.onAttendanceUpdate}
        />
      </>
    );
  }
}
