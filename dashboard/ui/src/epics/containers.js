import { Observable } from "rxjs";
import {
    TYPE_GET_CONTAINERS,
    getContainersSucceeded,
    getContainersFailed
} from "../actions/containers";

export function containersEpic(action$) {
    return action$.ofType(TYPE_GET_CONTAINERS).switchMap(action$ =>
        Observable.ajax
        .getJSON("/containers/user-api")
        .map(containers => getContainersSucceeded(containers))
        .catch(error => Observable.of(getContainersFailed(error)))
    );
}