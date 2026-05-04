import { useEffect, useState } from "react";
import { Alert, Button, Card, Form, Table } from "react-bootstrap";
import api from "../api";

export default function WishlistPage() {
  const [items, setItems] = useState([]);
  const [msg, setMsg] = useState("");

  const loadWishlist = () => {
    api.get("/wishlist/").then((response) => setItems(response.data));
  };

  useEffect(() => {
    loadWishlist();
  }, []);

  const removeItem = async (id) => {
    await api.delete(`/wishlist/${id}/`);
    loadWishlist();
  };

  const updateTargetPrice = async (id, targetPrice) => {
    await api.patch(`/wishlist/${id}/`, { target_price: targetPrice });
    setMsg("Target price saved.");
  };

  return (
    <Card>
      <Card.Body>
        <h3 className="mb-3">Wishlist</h3>
        {msg && <Alert variant="success">{msg}</Alert>}
        <Table responsive bordered hover>
          <thead>
            <tr>
              <th>Product</th>
              <th>Model</th>
              <th>Target Price</th>
              <th>Email Alert</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.product.name}</td>
                <td>{item.product.model_number}</td>
                <td>
                  <Form.Control
                    type="number"
                    defaultValue={item.target_price || ""}
                    placeholder="Set price"
                    onBlur={(e) => updateTargetPrice(item.id, e.target.value || null)}
                  />
                </td>
                <td>{item.notify_on_drop ? "Enabled" : "Disabled"}</td>
                <td>
                  <Button variant="danger" size="sm" onClick={() => removeItem(item.id)}>
                    Remove
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Card.Body>
    </Card>
  );
}
