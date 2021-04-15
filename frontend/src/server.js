import { createServer } from "miragejs";

export default function () {
  return createServer({
    routes() {
      this.get("http://localhost:8000/products/", () => [
        {
          id: 1,
          name: "Kefirek",
        },
        {
          id: 2,
          name: "kek",
        },
      ]);
    },
  });
}
