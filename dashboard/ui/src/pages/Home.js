import * as React from "react";
import { connect } from "react-redux";

import "./Home.css";
import {
  getDeployments
} from "../actions/deployments";
import DeploymentList from "../components/DeploymentList"

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    this.props.init();
  }

  render() {
    return (
      <div className="home container-fluid">
        <DeploymentList deployments={this.props.deployments} />
      </div>
    );
  }
}

function mapStateToProps(state) {
  return state.deploymentsReducer;
}

function mapDispatchToProps(dispatch) {
  return {
    init: () => {
      dispatch(getDeployments());
    }
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(Home);
