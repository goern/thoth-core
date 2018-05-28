import { combineReducers } from 'redux';
import { errorsReducer } from './errors';

const rootReducer = combineReducers({
  errorsReducer
});

export default rootReducer;
