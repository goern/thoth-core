import * as React from "react";
import { Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";

import "./MastHead.css";

const MastHead = (props) => {
  return (
    <Navbar fluid collapseOnSelect className="navbar navbar-pf-vertical">
      <Navbar.Header>
        <Navbar.Brand>
          <Link to="/">
              Thoth DevOps & SrcOps Dashboard
          </Link>
        </Navbar.Brand>
      </Navbar.Header>
    </Navbar>
  );
};

export default MastHead;
