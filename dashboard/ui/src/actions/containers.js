export const TYPE_GET_CONTAINERS = "GET_CONTAINERS";
export const getContainers = () => ({
  type: TYPE_GET_CONTAINERS,
  payload: {}
});

export const TYPE_GET_CONTAINERS_SUCCEEDED = "GET_CONTAINERS_SUCCEEDED";
export const getContainersSucceeded = (response) => ({
  type: TYPE_GET_CONTAINERS_SUCCEEDED,
  payload: {
    response
  }
});

export const TYPE_GET_CONTAINERS_FAILED = "GET_CONTAINERS_FAILED";
export const getContainersFailed = (error) => ({
  type: TYPE_GET_CONTAINERS_FAILED,
  payload: {
    error
  }
});