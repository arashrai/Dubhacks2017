import React, { Component } from 'react';

export default class Chat extends Component {
  state = {
    msg: "",
    chat: [],
    room: 0
  }

  componentDidMount() {
    window.socket.on('status', (data) => {
      console.log("on status", data)
      if (window.ROOM === data.room && window.OTHERBRAH !== data.username)
        this.setState({
          chat: [
            ...this.state.chat,
            {prefix: "",color: "black", msg: data.msg},
            {prefix: "",color:"green",msg:window.FUCKINGGLOBALSREEEEEEEE}
          ]
        })
    });

    window.socket.on('message', (data) => {
      console.log("on message", data)
      if (data.room === window.ROOM)
        this.setState({
          chat: [
            ...this.state.chat,
            {prefix: data.username + ": ", color: data.username === this.props.hoodis.username ? "blue" : "red", msg: data.msg}

          ]
        })
    });

    window.socket.on("decrementshow", (data) => {
          console.log(window.SHOW_CONTRA, this.props.hoodis.username, data)
      if (window.ROOM === data.room && this.props.hoodis.username === data.username) {
        window.SHOW_CONTRA--;
        if (window.SHOW_CONTRA === 0) {
          this.setState({
          chat: [
            ...this.state.chat,
            {prefix: "",color: "orange", msg: window.CONTRA},
          ]
        })
        }
      }
    })
  }

  handleType = (e) => {
    // If the user has pressed enter
    const text = e.target.value;
    if (text[text.length - 1] === "\n") {
      // this.setState({
      //   chat: [
      //     ...this.state.chat,
      //     {prefix: this.props.hoodis.username + ": ",color: "blue", msg: this.state.msg}
      //   ]
      // });

      window.socket.emit("text", {msg: this.state.msg, username: this.props.hoodis.username, room: window.ROOM})

      this.setState({msg: ""})
    } else {
      this.setState({msg: text.replace("\n", "")})
    }
  }

  render() {
    return (
      <div className="p-page p-chat">
        <h1>Talking with: {window.OTHERBRAH}</h1>
        <hr/>
        <div className="chat-window">
          {this.state.chat.map(({color, msg, prefix}) => {
            return (
              <div key={msg + prefix + color} style={{color: color}}>{prefix} {msg}</div>
            );
          })}
        </div>
        <hr/>
        <div onClick={() => {
          console.log(window.SHOW_CONTRA)
          if (window.DISABLE_REVEEEEL) return;
          window.DISABLE_REVEEEEL = "this code is cancer";
          window.SHOW_CONTRA--;
          if (window.SHOW_CONTRA === 0) {
            this.setState({
              chat: [
                ...this.state.chat,
                {prefix: "",color: "orange", msg: window.CONTRA},
              ]
            })
          }
          window.socket.emit("revealcontroversy", {
            room: window.ROOM,
            username: window.OTHERBRAH
          })
        }} className="le-grande-reveal">Where do we differ?</div>
        <textarea value={this.state.msg} onChange={this.handleType} />
      </div>
    );
  }
}
