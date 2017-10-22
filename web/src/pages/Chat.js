import React, { Component } from 'react';

export default class Chat extends Component {
  state = {
    msg: ""
  }

  handleType = (e) => {
    // If the user has pressed enter
    const text = e.target.value;
    if (text[text.length - 1] === "\n") {
      console.log("POST MSG")
      this.setState({msg: ""})
    } else {
      this.setState({msg: text.trim()})
    }
  }

  render() {
    return (
      <div className="p-page p-chat">
        <h1>Talking with: {"Billy. J"}</h1>
        <hr/>
        <div className="chat-window">

        </div>
        <hr/>
        <div className="le-grande-reveal">Where do we differ?</div>
        <textarea value={this.state.msg} onChange={this.handleType} />
      </div>
    );
  }
}
