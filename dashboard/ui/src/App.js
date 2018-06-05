import React, { Component } from "react";
import { withRouter } from "react-router-dom";

import MastHead from "./components/MastHead";
import { Routes } from "./Routes"

import "../node_modules/patternfly/dist/css/patternfly.css";
import "../node_modules/patternfly/dist/css/patternfly-additions.css";
import "../node_modules/patternfly-react/dist/css/patternfly-react.css";
import "./App.css";

class App extends Component {
  handleTitleClick = () => {
  };
  handleNavToggle = () => {
  };

  render() {
    return (
      <div className="App">
        <MastHead />
        <Routes/>
      </div>
    );
  }
}

export default withRouter(App);
