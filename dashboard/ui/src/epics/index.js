import { combineEpics } from "redux-observable";
import { containersEpic } from "./containers";

export const rootEpic = combineEpics(
  containersEpic
);
