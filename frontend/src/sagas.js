import {takeEvery} from 'redux-saga/effects';

function* handleInit(action){
    console.log("Poszło init!");
}

function* mySaga(){
    yield takeEvery("@@INIT", handleInit);
}

export default mySaga;