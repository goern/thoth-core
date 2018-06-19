import { Observable } from "rxjs";
import {
    TYPE_GET_DEPLOYMENTS,
    getDeploymentsSucceeded,
    getDeploymentsFailed
} from "../actions/deployments";

export function deploymentsEpic(action$) {
    return action$.ofType(TYPE_GET_DEPLOYMENTS).switchMap(action$ =>
        Observable.ajax
        .getJSON("/containers/user-api")
        .map(deployments => getDeploymentsSucceeded(deployments))
        .catch(error => Observable.of(getDeploymentsFailed(error)))
    );
}