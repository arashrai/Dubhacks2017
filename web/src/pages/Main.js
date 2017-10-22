import React, { Component } from 'react';

const sleep = x => new Promise(res => setTimeout(res, x));

export default class Main extends Component {
  state = {
    text: "Let's talk!"
  }

  findChat = async () => {
    console.log("do thing")

    await sleep(500);
    this.setState({text: "Found someone!"})
    await sleep(2000);

    this.props.gotoPage("Chat")

    console.log("goto chat")
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
    this.setState({text: "Matching."})
    await sleep(300);
    this.setState({text: "Matching.."})
    await sleep(300);
    this.setState({text: "Matching..."})
    await sleep(300);
    this.setState({text: "Matching."})
    await sleep(300);
    this.setState({text: "Matching.."})
    await sleep(300);
    this.setState({text: "Matching..."})
    await sleep(300);
    this.setState({text: "Matching."})
    await sleep(300);
    this.setState({text: "Matching.."})
    await sleep(300);
    this.setState({text: "Matching..."})

    this.findChat()
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
