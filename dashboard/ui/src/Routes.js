import * as React from 'react';
import { Route, Switch } from 'react-router-dom';
import asyncComponent from './components/Router/AsyncComponent';
import { AuthenticatedRoute } from './components/Router/AuthenticatedRoute';
import { UnauthenticatedRoute } from './components/Router/UnauthenticatedRoute';

const importHome = asyncComponent(() =>
    import ('./pages/Home'));
const importNotFound = asyncComponent(() =>
    import ('./pages/NotFound'));

type Props = {
    childProps: any
};
export const Routes = (props: Props) => {
    return ( <
        Switch >
        <
        UnauthenticatedRoute path = "/"
        exact component = { importHome }
        props = { props.childProps }
        />

        { /* Finally, catch all unmatched routes */ } <
        Route component = { importNotFound }
        /> <
        /Switch>
    );
};