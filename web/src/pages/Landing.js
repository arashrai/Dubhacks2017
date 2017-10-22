import React, { Component } from 'react';

export default class Landing extends Component {
  render() {
    return (
      <div className="p-page p-login">
        <div onClick={() => this.props.gotoPage("Main")} className="btn btn-login">SKIP TO MAIN</div>
        <div onClick={() => this.props.gotoPage("Chat")} className="btn btn-login">SKIP TO CHAT</div>
        <h1>AcrossTheAisle</h1>
        <div className="t-subtitle">Humanizing one another, one conversation at a time</div>
        <hr/>
        <div>
          <p>We want you to have a conversation with someone who you might never have thought to talk to!</p>
          <p>We match you with someone who we think is a lot like you, but disagrees with you on one hot-button issue. The catch: we don't tell you which one! Before telling you where you differ, we start off by telling how you two are alike. Start off the conversation talking about your shared hobbies, interests, and ambitions, and only once both of you think you've gotten to know eachother can you can hit the reveal button and find you where you disagree.</p>
          <p>Hopefully, by getting to know one another, and humanizing eachother, you can have a interesting discussion about your difference, and be more receptive to hear what someone across the aisle has to say.</p>
          <p>After all, we are all humans :)</p>
        </div>
        <hr/>
        <div onClick={() => this.props.gotoPage("Login")} className="btn btn-login">Login</div>
        <div onClick={() => this.props.gotoPage("Signup")} className="btn btn-signup">Join</div>
        <div className="footer">
          Made with {'<'}3 at <a className="dubhacks" href="http://dubhacks.co/">dubhacks 2017</a>
        </div>
      </div>
    );
  }
}
