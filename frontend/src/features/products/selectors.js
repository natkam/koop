import { createSelector } from "@reduxjs/toolkit";

const coolOrders = createSelector(
  (state) => state,
  (state) => {
    return state.products.order.filter((product) => product.quantity > 0);
  }
);

export { coolOrders };
