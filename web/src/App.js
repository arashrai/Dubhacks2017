import React, { Component } from 'react';

import Chat from './pages/Chat';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Main from './pages/Main';

const page_map = {
  Chat, Landing, Login, Main
}

class App extends Component {
  state = {
    curr_page: "Landing"
  }

  componentDidMount() {
    window.history.pushState({page: "Landing"}, "Landing", "/");
    window.addEventListener("popstate", ({state}) => {
      this.setState({curr_page: state.page})
    })
  }

  gotoPage = (page) => {
    window.history.pushState({page: page}, page, page === "Landing" ? "/" : page.toLowerCase());
    this.setState({curr_page: page});
  }

  render() {
    const Page = page_map[this.state.curr_page];
    return <Page gotoPage={this.gotoPage} />;
  }
}

export default App;
