import React from 'react';
import { useSelector } from "react-redux";

const ProductTable = props => {
    const products = useSelector(state => state.products.products);
    return <>
        <table>
            <tbody>
            {
                products.map(product => <tr key={product.id}><td>{product.name}</td></tr>)
            }
            </tbody>
        </table>
    </>

}

export { ProductTable }