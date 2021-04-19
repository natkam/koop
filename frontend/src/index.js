import "babel-polyfill";
import React from "react";
import { render } from "react-dom";
import { Provider } from "react-redux";
import { store } from "./store";
import { ProductTable } from "./features/products/productTable";
import { Container } from "react-bootstrap";

const App = () => {
  return (
    <>
      <Container>
        <ProductTable></ProductTable>
      </Container>
    </>
  );
};

render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
