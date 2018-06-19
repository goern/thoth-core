import { combineEpics } from "redux-observable";
import {
  deploymentsEpic
}
from "./deployments";

export const rootEpic = combineEpics(
  deploymentsEpic
);
