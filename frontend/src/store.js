import { configureStore, MiddlewareArray } from "@reduxjs/toolkit";
import createSagaMiddleware from "redux-saga";
import mySaga from "./sagas";
import productReducer from "./features/products/productSlice";
import mirageServer from "./server";

mirageServer();

const sagaMiddleware = createSagaMiddleware();

const store = configureStore({
  reducer: {
    products: productReducer,
  },
  middleware: new MiddlewareArray().concat(sagaMiddleware),
});

sagaMiddleware.run(mySaga);
store.dispatch({ type: "FETCH_PRODUCTS" });

export { store };
