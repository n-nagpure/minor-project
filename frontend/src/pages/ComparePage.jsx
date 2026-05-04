import { useState } from "react";
import { Alert, Badge, Button, Card, Col, Form, Row, Table } from "react-bootstrap";
import api from "../api";

export default function ComparePage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // List of common platforms for fallback display
  const FALLBACK_PLATFORMS = ["amazon", "flipkart", "croma", "reliance"];

  const search = async (event) => {
    event.preventDefault();
    setLoading(true);
    setMessage("Fetching latest platform prices...");
    try {
      const response = await api.get(`/products/compare/?q=${encodeURIComponent(query)}`);
      setResults(response.data);
      setMessage(response.data.length ? "Showing latest available prices." : "No products found for this model.");
    } catch (error) {
      setMessage("Unable to fetch live prices right now. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const addToWishlist = async (productId) => {
    try {
      await api.post("/wishlist/", { product_id: productId, notify_on_drop: true });
      setMessage("Added to wishlist.");
    } catch (error) {
      setMessage("Login first or product already in wishlist.");
    }
  };

  const hasAvailablePrices = (prices) => prices && prices.length > 0;

  const getDisplayPrices = (prices) => {
    // If prices exist, return them as-is
    if (hasAvailablePrices(prices)) {
      return prices;
    }
    // If no prices, show out-of-stock for all platforms
    return FALLBACK_PLATFORMS.map((platform, index) => ({
      id: `fallback-${index}`,
      source: platform,
      price: null,
      buy_url: null,
      in_stock: false,
      fetched_at: null,
      status_message: "Out of Stock",
    }));
  };

  const handleImageError = (e) => {
    e.currentTarget.src = "https://via.placeholder.com/80x80/cccccc/666666?text=No+Image";
  };

  return (
    <>
      <Card className="mb-4">
        <Card.Body>
          <h3>Compare Product Prices</h3>
          <p className="text-muted mb-3">Search by product name or model number.</p>
          <Form onSubmit={search}>
            <Row className="g-2">
              <Col md={10}>
                <Form.Control
                  placeholder="Example: A3090 or iPhone 15"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  required
                />
              </Col>
              <Col md={2}>
                <Button className="w-100" type="submit" disabled={loading}>
                  {loading ? "Loading..." : "Search"}
                </Button>
              </Col>
            </Row>
          </Form>
        </Card.Body>
      </Card>

      {message && <Alert variant="info">{message}</Alert>}

      {results.map((product) => (
        <Card key={product.id} className="mb-3">
          <Card.Body>
            <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-2">
              <div className="d-flex align-items-center gap-3">
                <div className="product-image-container">
                  <img
                    src={product.image_url || "https://via.placeholder.com/80x80/cccccc/666666?text=No+Image"}
                    alt={product.name}
                    className="product-image"
                    onError={handleImageError}
                  />
                </div>
                <div>
                  <h5 className="mb-1">{product.name}</h5>
                  <div className="text-muted">
                    Model: {product.model_number} | Brand: {product.brand}
                  </div>
                </div>
              </div>
              <div className="d-flex gap-2 align-items-center">
                <Badge bg={hasAvailablePrices(product.prices) ? "success" : "danger"}>
                  {hasAvailablePrices(product.prices)
                    ? `Lowest: INR ${product.lowest_price || "N/A"}`
                    : "Out of Stock"}
                </Badge>
                <Button size="sm" onClick={() => addToWishlist(product.id)}>
                  Add Wishlist
                </Button>
              </div>
            </div>
            <Table responsive bordered hover>
              <thead>
                <tr>
                  <th>Platform</th>
                  <th>Price</th>
                  <th>Status</th>
                  <th>Buy</th>
                </tr>
              </thead>
              <tbody>
                {getDisplayPrices(product.prices).map((offer) => (
                  <tr key={offer.id}>
                    <td className="text-capitalize">{offer.source}</td>
                    <td>{offer.price ? `INR ${offer.price}` : "N/A"}</td>
                    <td>{offer.status_message || (offer.in_stock ? "In Stock" : "Out of Stock")}</td>
                    <td>
                      {offer.buy_url ? (
                        <a href={offer.buy_url} target="_blank" rel="noreferrer">
                          Buy Now
                        </a>
                      ) : (
                        <span className="text-muted">Not available</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
      ))}
    </>
  );
}
