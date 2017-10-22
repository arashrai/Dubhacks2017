import React, { Component } from 'react';

export default class Landing extends Component {
  render() {
    return (
      <div className="p-page p-landing">
        <h1>AcrossTheAisle</h1>
        <div className="t-subtitle">Humanizing one another, one conversation at a time</div>
        <hr/>
        <div>
          <p>We want you to have a conversation with someone who you might never have thought to talk to!</p>
          <p>AcrossTheAisle matches you with someone who is a lot like you, sharing similar hobbies, interests, and ambitions, but who also disagrees with you on <em>some</em> hot-button issue. But here's the thing: we don't tell you what you disagree on until after you've both had a chance to bond over mutual experiences!</p>
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
