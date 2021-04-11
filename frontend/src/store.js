import { createStore, applyMiddleware} from 'redux';
import createSagaMiddleware from 'redux-saga';
import mySaga from './sagas';

function reducer(state, action) {
    return {};
}

const sagaMiddleware = createSagaMiddleware()
const store = createStore(reducer,
    applyMiddleware(sagaMiddleware));

sagaMiddleware.run(mySaga)
store.dispatch({type: "@@INIT"});

export {store};
