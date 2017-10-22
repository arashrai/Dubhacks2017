import React, { Component } from 'react';

const questions = {
  question_one: "Where are you from?",
  question_two: "pebis or vahine?",
  // q3: "do u laik nazis?"
}

export default class Signup extends Component {
  state = {
    username: "",
    password: "",
    email: "",
    survey: {}
  }

  SIGNMETHEFUCKUPMMHMMMHHMGOODSHITDATSSOMEGOODSHITRIGHTTHERE = () => {
    this.props.updateUserDeets({username: this.state.username, password: this.state.password})

    var data = JSON.stringify(this.state);

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

    xhr.open("POST", "http://arashrai.com:5000/signup");
    xhr.setRequestHeader("content-type", "application/json");
    xhr.setRequestHeader("cache-control", "no-cache");

    xhr.send(data);
  }

  render() {
    return (
      <div className="p-page p-signup">
        <h1>Hi There!</h1>
        <p>Let's get your account set up!</p>
        <div className="signup-form">
          <div className="form-group">
            <input value={this.state.username} onChange={(e) => this.setState({username: e.target.value})} type="text" required="required"/>
            <label className="control-label" htmlFor="input">Username</label><i className="bar"></i>
          </div>
          <div className="form-group">
            <input value={this.state.password} onChange={(e) => this.setState({password: e.target.value})} type="password" required="required"/>
            <label className="control-label" htmlFor="input">Password</label><i className="bar"></i>
          </div>
          <div className="form-group">
            <input value={this.state.email} onChange={(e) => this.setState({email: e.target.value})} type="text" required="required"/>
            <label className="control-label" htmlFor="input">Email</label><i className="bar"></i>
          </div>
        </div>
        <p>Now that that's out of the way, tell us a bit about yourself!</p>
        {(() => {
          return Object.keys(questions).reduce((a, key) => {
            const question = questions[key];
            return a.concat(
              <div className="form-group" key={key}>
                <input
                  value={this.state.survey[key]}
                  onChange={(e) => this.setState({
                    survey: {
                      ...this.state.survey,
                      [key]: e.target.value}
                    })
                  }
                  type="text"
                  required="required"
                />
                <label className="control-label" htmlFor="input">{question}</label><i className="bar"></i>
              </div>
            )
          }, [])
        })()}
        {this.state.error &&
          <div style={{
            color: "#E91E63",
            textAlign: "center",
            fontSize: "14px",
          }}>Uh oh, looks like the username "{this.state.username}" is taken :(</div>
        }
        <div
          onClick={this.SIGNMETHEFUCKUPMMHMMMHHMGOODSHITDATSSOMEGOODSHITRIGHTTHERE}
          className="btn btn-signup">Submit</div>
      </div>
    );
  }
}
