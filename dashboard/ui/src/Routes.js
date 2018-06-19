import React from "react";
import {
  Switch,
  Route,
} from "react-router-dom";

import Home from "./pages/Home"
import NotFound from "./pages/NotFound";

export const Routes = () => (
  <Switch>
    <Route path="/" exact component={ Home } />
    <Route component={ NotFound } />
  </Switch>
);
