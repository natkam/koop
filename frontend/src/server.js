import { createServer } from "miragejs";

export default function () {
  return createServer({
    routes() {
      // What is the current state of the order for this week
      this.get("http://localhost:8000/weeks/latest/order/", () => [
        {
          id: 1,
          name: "KEKS",
          quantity: 1,
        },
        {
          id: 2,
          name: "Kefirek",
          quantity: 3,
        },
        {
          id: 3,
          name: "Jagódki",
          quantity: 0,
        },
      ]);

      this.post("http://localhost:8000/weeks/latest/order/", () => {});
    },
  });
}
