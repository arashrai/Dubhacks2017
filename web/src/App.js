import React, { Component } from 'react';

import Chat from './pages/Chat';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Main from './pages/Main';
import Signup from './pages/Signup';

const page_map = {
  Chat, Landing, Login, Main, Signup
}

class App extends Component {
  state = {
    curr_page: "Landing",
    user: {
      username: "testuser",
      password: "test"
    }
  }

  componentDidMount() {
    window.history.pushState({page: "Landing"}, "Landing", "/");
    window.addEventListener("popstate", ({state}) => {
      this.setState({curr_page: state.page})
    })
  }

  updateUserDeets = (user) => {
    this.setState({user})
  }


  gotoPage = (page) => {
    window.history.pushState({page: page}, page, page === "Landing" ? "/" : page.toLowerCase());
    this.setState({curr_page: page});
  }

  render() {
    const Page = page_map[this.state.curr_page];
    // yolo just give every page every function ezpz
    return <Page hoodis={this.state.user} updateUserDeets={this.updateUserDeets} gotoPage={this.gotoPage} />;
  }
}

export default App;
