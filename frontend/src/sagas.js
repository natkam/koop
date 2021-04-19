import { takeEvery } from "redux-saga/effects";
import { fetchOrder, updateOrder } from "./features/products/sagas";

function* mySaga() {
  yield takeEvery("FETCH_ORDER", fetchOrder);
  yield takeEvery("UPDATE_ORDER", updateOrder);
}

export default mySaga;
