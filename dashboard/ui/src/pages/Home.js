import * as React from "react";
import { connect } from "react-redux";

import "./Home.css";
import { getContainers } from "../actions/containers";
import ContainerList from "../components/ContainerList"

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
        <ContainerList containers={this.props.containers} />
      </div>
    );
  }
}

function mapStateToProps(state) {
  return state.containersReducer;
}

function mapDispatchToProps(dispatch) {
  return {
    init: () => {
      dispatch(getContainers());
    }
  };
}


export default connect(mapStateToProps, mapDispatchToProps)(Home);
