import { all, fork, put } from 'redux-saga/effects';

function* rootSaga() {
    // yield all([fork(login), put(initCredentials())]);
}

export default rootSaga;