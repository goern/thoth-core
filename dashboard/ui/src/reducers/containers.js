import {
  TYPE_GET_CONTAINERS,
  TYPE_GET_CONTAINERS_SUCCEEDED,
  TYPE_GET_CONTAINERS_FAILED
} from "../actions/containers";


const initialState = {
  containers: [],
  containersLoading: false,
  containersLoadingError: null
};

export const containersReducer = (state = initialState, action) => {
  console.log(containersReducer);
  console.log(action);
  switch (action.type) {
    case TYPE_GET_CONTAINERS:
      return {
        ...state,
        containersLoading: true
      };
    case TYPE_GET_CONTAINERS_SUCCEEDED:
      return {
        ...state,
        containers: action.payload.response,
        containersLoading: false,
        containersLoadingError: null
      };
    case TYPE_GET_CONTAINERS_FAILED:
      console.error(action.payload.error);
      return {
        ...state,
        containers: [],
        containersLoading: false,
        containersLoadingError: action.payload.error
      };
    default:
      return state;
  }
};
