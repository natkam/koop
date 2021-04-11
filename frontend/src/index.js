import "babel-polyfill";
import React, { useState } from "react";
import { render } from "react-dom";
import { Provider } from 'react-redux';
import { store } from './store';


function App() {
    const [state, setState] = useState("CLICK");
    return <>
        <button onClick={() => setState("CLICKED")}>Super guzik</button>
    </>
}

render(<Provider store={store}><App /></Provider>, document.getElementById("root"));