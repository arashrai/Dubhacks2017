import React, { Component } from 'react';

export default class Chat extends Component {
  render() {
    return (
      <div className="p-chat">
        Chat Page
        <button onClick={() => this.props.gotoPage("Landing")}>goto landing</button>
        <button onClick={() => this.props.gotoPage("Main")}>goto main</button>
      </div>
    );
  }
}
