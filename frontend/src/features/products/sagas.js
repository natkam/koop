import { put } from "redux-saga/effects";
import { setProducts } from "./productSlice";

function* fetchProducts() {
  fetch("http://localhost:8000/products/").then((response) => {
    response.json().then((data) => {
      console.log(data);
    });
  });
  const response = yield fetch("http://localhost:8000/products/");
  const products = yield response.json();

  yield put(setProducts(products));
}

export { fetchProducts };
