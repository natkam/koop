import "babel-polyfill";
import React from "react";
import { render } from "react-dom";
import { Provider } from 'react-redux';
import { store } from './store';
import {ProductTable} from "./features/products/productTable";


const App = () => {
    return <>
        <ProductTable></ProductTable>
    </>
}

render(<Provider store={store}><App /></Provider>, document.getElementById("root"));
