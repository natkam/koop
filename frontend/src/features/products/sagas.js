import { put } from "redux-saga/effects";
import { setOrder } from "./productSlice";

function* fetchOrder() {
  const response = yield fetch("http://localhost:8000/weeks/latest/order/");
  const order = yield response.json();

  yield put(setOrder(order));
}

function* updateOrder(action) {
  const payload = action.payload;
  const response = yield fetch("http://localhost:8000/weeks/latest/order/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  yield response.json();

  if (response.ok) {
    yield put({ type: "FETCH_ORDER" });
  }
}

export { fetchOrder, updateOrder };
