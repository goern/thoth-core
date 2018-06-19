import {
    TYPE_GET_DEPLOYMENTS,
    TYPE_GET_DEPLOYMENTS_SUCCEEDED,
    TYPE_GET_DEPLOYMENTS_FAILED
} from "../actions/deployments";


const initialState = {
    deployments: [],
    deploymentsLoading: false,
    deploymentsLoadingError: null
};

export const deploymentsReducer = (state = initialState, action) => {
    console.log(deploymentsReducer);
    console.log(action);
    
    switch (action.type) {
        case TYPE_GET_DEPLOYMENTS:
            return {
                ...state,
                deploymentsLoading: true
            };
        case TYPE_GET_DEPLOYMENTS_SUCCEEDED:
            return {
                ...state,
                deployments: action.payload.response,
                deploymentsLoading: false,
                deploymentsLoadingError: null
            };
        case TYPE_GET_DEPLOYMENTS_FAILED:
            console.error(action.payload.error);
            return {
                ...state,
                deployments: [],
                deploymentsLoading: false,
                deploymentsLoadingError: action.payload.error
            };
        default:
            return state;
    }
};