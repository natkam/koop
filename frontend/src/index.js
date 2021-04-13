import "babel-polyfill";
import React, { useState } from "react";
import { render } from "react-dom";
import { Provider } from 'react-redux';
import { store } from './store';
import {ProductTable} from "./features/products/productTable";


const App = () => {
    const [state, setState] = useState(0);

    return <>
        <ProductTable></ProductTable>
        <button onClick={() => setState(state + 1)}>{state}</button>
    </>
}

render(<Provider store={store}><App /></Provider>, document.getElementById("root"));