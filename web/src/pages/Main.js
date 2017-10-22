import React, { Component } from 'react';

const sleep = x => new Promise(res => setTimeout(res, x));

export default class Main extends Component {
  state = {
    text: "Let's talk!"
  }

  startLoading = async () => {
    this.setState({text: "Connecting."})
    await sleep(300);
    this.setState({text: "Connecting.."})
    await sleep(300);
    this.setState({text: "Connecting..."})
    await sleep(300);
    this.setState({text: "Connecting."})
    await sleep(300);

    window.socket = window.io.connect('http://arashrai.com:5000/chat');

    window.socket.on('connect', () => {
      console.log("on connect")
      window.ROOM = null;
      window.socket.emit('lookingforgroup', {username: this.props.hoodis.username});
    });

    window.socket.on('joinroom', (data) => {

      console.log("on joinroom", data);
      window.OTHERBRAH = data.user1 === this.props.hoodis.username ? data.user2 : data.user1;
      if(window.ROOM === null){
      window.FUCKINGGLOBALSREEEEEEEE = data.common;
        window.CONTRA = data.controversy;
        window.SHOW_CONTRA = 2;
        window.ROOM = data.room;
      } // wiring state is harddddd
      window.socket.emit('actuallyjoinroom', {username: this.props.hoodis.username, room: data.room});
    });

    // i want to die
    var doit = true;
    window.socket.on('joinroom', () => {
      console.log("on joinroom - doit")
      doit = false;
    })
    while (doit) {
      this.setState({text: "Matching."})
      await sleep(300);
      this.setState({text: "Matching.."})
      await sleep(300);
      this.setState({text: "Matching..."})
      await sleep(300);
    }

    this.setState({text: "Found someone!"})
      this.props.gotoPage("Chat")
    await sleep(2000);
  }

  render() {
    return (
      <div className="p-page p-main">
        <div onClick={this.startLoading} className="find-chat">
          {this.state.text}
        </div>
      </div>
    );
  }
}
