import { put } from 'redux-saga/effects';
import {addProduct} from "./productsSlice";

function* fetchProducts() {
    const response = yield fetch("http://localhost:8000/products/");
    const products = yield response.json();

    for(let x = 0; x < products.length; x++){
        yield put(addProduct(products[x]));
    }
}

export { fetchProducts };