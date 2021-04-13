import {takeEvery, takeLatest, put} from 'redux-saga/effects';
import {fetchProducts} from "./features/products/sagas";

function* handleInit(action, dispatch){
    console.log("Poszło init!");
    yield put({type: "FETCH_PRODUCTS"});
}


function* mySaga(){
    yield takeEvery("@@INIT", handleInit);
    yield takeEvery("FETCH_PRODUCTS", fetchProducts);
}

export default mySaga;