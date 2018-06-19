export const TYPE_GET_DEPLOYMENTS = "GET_DEPLOYMENTS";
export const getDeployments = () => ({
    type: TYPE_GET_DEPLOYMENTS,
    payload: {}
});

export const TYPE_GET_DEPLOYMENTS_SUCCEEDED = "GET_DEPLOYMENTS_SUCCEEDED";
export const getDeploymentsSucceeded = (response) => ({
    type: TYPE_GET_DEPLOYMENTS_SUCCEEDED,
    payload: {
        response
    }
});

export const TYPE_GET_DEPLOYMENTS_FAILED = "GET_DEPLOYMENTS_FAILED";
export const getDeploymentsFailed = (error) => ({
    type: TYPE_GET_DEPLOYMENTS_FAILED,
    payload: {
        error
    }
});