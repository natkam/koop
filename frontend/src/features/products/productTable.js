import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import { Formik } from "formik";

const ProductTable = () => {
  const order = useSelector((state) => state.products.order);
  const dispatch = useDispatch();
  const initialValues = {};

  useEffect(() => {
    dispatch({ type: "FETCH_ORDER" });
  }, []);

  if (order) {
    order.map((product) => {
      initialValues[product.id] = product.quantity;
    });
  }

  return order ? (
    <Formik
      initialValues={initialValues}
      onSubmit={(values) => {
        dispatch({ type: "UPDATE_ORDER", payload: values });
      }}
    >
      {({ handleSubmit, handleChange, values }) => (
        <Form onSubmit={handleSubmit}>
          <Table striped bordered hover variant="dark" size="sm">
            <thead>
              <tr>
                <th>Nazwa</th>
                <th>Zamawiana ilość</th>
              </tr>
            </thead>
            <tbody>
              {order
                ? order.map((product) => (
                    <tr key={product.id}>
                      <td>{product.name}</td>
                      <td>
                        <Form.Group controlId="amount">
                          <Form.Control
                            name={product.id}
                            type="number"
                            placeholder="Ilość"
                            value={values[product.id]}
                            onChange={handleChange}
                          />
                        </Form.Group>
                      </td>
                    </tr>
                  ))
                : null}
            </tbody>
          </Table>
          <Button variant="primary" type="submit">
            Złóż zamówienie
          </Button>
        </Form>
      )}
    </Formik>
  ) : null;
};

export { ProductTable };
