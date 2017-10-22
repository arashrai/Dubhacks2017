import React, { Component } from 'react';

export default class Main extends Component {
  render() {
    return (
      <div className="p-page p-main">
        <h1>AcrossTheAisle</h1>
        <div className="find-chat-person">

        </div>
        <button onClick={() => this.props.gotoPage("Landing")}>goto landing</button>
        <button onClick={() => this.props.gotoPage("Chat")}>goto chat</button>
      </div>
    );
  }
}
