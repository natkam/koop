import {takeEvery, takeLatest, put} from 'redux-saga/effects';
import {fetchProducts} from "./features/products/sagas";

function* mySaga(){
    yield takeEvery("FETCH_PRODUCTS", fetchProducts);
}

export default mySaga;