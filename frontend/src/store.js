import {configureStore, MiddlewareArray} from "@reduxjs/toolkit";
import createSagaMiddleware from 'redux-saga';
import mySaga from './sagas';
import productReducer from './features/products/productsSlice';

const sagaMiddleware = createSagaMiddleware()

const store = configureStore({
    reducer: {
        products: productReducer
    },
    middleware: new MiddlewareArray().concat(sagaMiddleware)
})

sagaMiddleware.run(mySaga)
store.dispatch({type: "@@INIT"});

export {store};
