import * as React from 'react';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Alert } from 'patternfly-react';

const logo = require('../logo.svg');

interface State {
  alertVisible: boolean;
}
class HomePage extends React.Component<RouteComponentProps<any>, State> {
  constructor(props: any) {
    super(props);

    this.state = {
      alertVisible: true
    };
  }

  dismissAlert = () => {
    this.setState({ alertVisible: false });
  };

  render() {
    return (
      <div className="container-fluid container-pf-nav-pf-vertical">
        <div className="page-header">
          <h2>Overview</h2>
        </div>
        <div className="App-body">
          <p className="App-paragraph">
            To get started, edit ...
          </p>
        </div>
      </div>
    );
  }
}

export default withRouter(HomePage);
