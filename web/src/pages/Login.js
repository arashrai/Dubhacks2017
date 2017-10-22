import React, { Component } from 'react';

export default class Login extends Component {
  state = {
    username: "",
    password: "",
    error: false,
  }

  plslogin = () => {
    this.props.updateUserDeets({username: this.state.username, password: this.state.password})

    var data = JSON.stringify({
      "username": this.state.username,
      "password": this.state.password,
    });

    var xhr = new XMLHttpRequest();

    const self = this;
    xhr.addEventListener("readystatechange", function () {
      if (this.readyState === 4) {
        if (this.responseText.trim() === "true") {
          self.props.gotoPage("Main");
        } else {
          self.setState({error: true})
        }
      }
    });

    xhr.open("POST", "http://arashrai.com:5000/login");
    xhr.setRequestHeader("content-type", "application/json");
    xhr.setRequestHeader("cache-control", "no-cache");

    xhr.send(data);
  }

  render() {
    return (
      <div className="p-page p-login">
        <h1>Welcome Back!</h1>
        <div className="login-form">
          <div className="form-group">
            <input value={this.state.username} onChange={(e) => this.setState({username: e.target.value})} type="text" required="required"/>
            <label className="control-label" htmlFor="input">Username</label><i className="bar"></i>
          </div>
          <div className="form-group">
            <input value={this.state.password} onChange={(e) => this.setState({password: e.target.value})} type="password" required="required"/>
            <label className="control-label" htmlFor="input">Password</label><i className="bar"></i>
          </div>
        </div>
        {this.state.error &&
          <div style={{
            color: "#E91E63",
            textAlign: "center",
            fontSize: "14px",
          }}>Uh oh, looks like your login details were wrong :(</div>
        }
        <div onClick={this.plslogin} className="btn btn-login">Login</div>
      </div>
    );
  }
}
