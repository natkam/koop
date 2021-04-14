import React from "react";
import { useSelector } from "react-redux";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";

const ProductTable = () => {
  const products = useSelector((state) => state.products.products);
  return (
    <>
      <Table striped bordered hover variant="dark" size="sm">
        <thead>
          <tr>
            <th>Nazwa</th>
            <th>Zamawiana ilość</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td>{product.name}</td>
              <td>
                <Form>
                  <Form.Group controlId="amount">
                    <Form.Control type="number" placeholder="Ilość" />
                  </Form.Group>
                </Form>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      <Button>Złóż zamówienie</Button>
    </>
  );
};
export { ProductTable };
