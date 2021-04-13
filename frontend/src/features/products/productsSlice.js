import { createSlice } from '@reduxjs/toolkit';

export const productsSlice = createSlice({
    name: "products",
    initialState: {
        products: [],
    },
    reducers: {
        addProduct: (state, product) => {
            state.products.push(product.payload);
        },
    }
})

export const { addProduct } = productsSlice.actions;
export default productsSlice.reducer;