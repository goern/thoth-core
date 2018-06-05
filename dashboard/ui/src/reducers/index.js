import { combineReducers } from "redux";
import { containersReducer } from "./containers";

const rootReducer = combineReducers({
  containersReducer
});

export default rootReducer;
