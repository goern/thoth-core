import * as React from 'react';
import { Nav, Navbar } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const pfLogo = require('../../img/logo-alt.svg');
const pfBrand = require('../../img/brand-alt.svg');

interface Props {}

export const MastHead: React.StatelessComponent<Props> = props => {
  return (
    <Navbar fluid collapseOnSelect className="navbar navbar-pf-vertical">
      <Navbar.Header>
        <Navbar.Brand>
          <Link to="/">
            <img className="navbar-brand-icon" src={pfLogo} alt="" />
              Thoth DevOps & SrcOps Dashboard
          </Link>
        </Navbar.Brand>
      </Navbar.Header>
    </Navbar>
  );
};
