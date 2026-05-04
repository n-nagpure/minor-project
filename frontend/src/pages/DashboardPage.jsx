import { useEffect, useState } from "react";
import { Alert, Button, Card, Col, Form, Row } from "react-bootstrap";
import api from "../api";

export default function DashboardPage() {
  const [data, setData] = useState({ 
    wishlist_count: 0, 
    compared_products: 0, 
    username: "", 
    first_name: "", 
    last_name: "" 
  });
  const [profile, setProfile] = useState({ 
    username: "", 
    first_name: "", 
    last_name: "", 
    email: "", 
    new_password: "", 
    confirm_password: "" 
  });

  const [status, setStatus] = useState({ error: "", success: "" });
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const extractErrorMessage = (error) => {
    const payload = error?.response?.data;
    if (!payload) return "Unable to update profile.";
    if (typeof payload === "string") return payload;
    if (payload.detail) return payload.detail;
    const lines = Object.entries(payload).flatMap(([key, values]) => {
      const list = Array.isArray(values) ? values : [values];
      return list.map((v) => `${key}: ${v}`);
    });
    return lines.join(" | ");
  };

  useEffect(() => {
    api.get("/dashboard/").then((response) => {
      console.log("Dashboard API response:", response.data);
      setData({
        username: response.data.username || "",
        first_name: response.data.first_name || "",
        last_name: response.data.last_name || "",
        wishlist_count: response.data.wishlist_count || 0,
        compared_products: response.data.compared_products || 0,
      });
    }).catch(err => console.error("Dashboard API error:", err));
    
    api.get("/profile/").then((response) => {
      console.log("Profile API response:", response.data);
      setProfile({
        username: response.data.username || "",
        first_name: response.data.first_name || "",
        last_name: response.data.last_name || "",
        email: response.data.email || "",
        new_password: "",
        confirm_password: ""
      });
    }).catch(err => console.error("Profile API error:", err));
  }, []);

  const handleUpdateProfile = async (event) => {
    event.preventDefault();
    setStatus({ error: "", success: "" });
    if (profile.new_password && profile.new_password !== profile.confirm_password) {
      setStatus({ error: "confirm_password: Passwords do not match.", success: "" });
      return;
    }
    try {
      const response = await api.patch("/profile/", profile);
      const updatedProfile = response.data;
      setStatus({ error: "", success: "Profile updated successfully." });
      localStorage.setItem("username", updatedProfile.username);
      localStorage.setItem("first_name", updatedProfile.first_name || "");
      localStorage.setItem("last_name", updatedProfile.last_name || "");
      setData((prev) => ({
        ...prev,
        first_name: updatedProfile.first_name || prev.first_name,
        last_name: updatedProfile.last_name || prev.last_name,
        username: updatedProfile.username || prev.username,
      }));
      setProfile({
        username: updatedProfile.username || "",
        first_name: updatedProfile.first_name || "",
        last_name: updatedProfile.last_name || "",
        email: updatedProfile.email || "",
        new_password: "",
        confirm_password: "",
      });
    } catch (error) {
      setStatus({ error: extractErrorMessage(error), success: "" });
    }
  };

  return (
    <>
      <h3 className="mb-3">
        Welcome, {data.first_name && data.last_name 
          ? `${data.first_name} ${data.last_name}` 
          : data.username}
      </h3>
      <Row className="g-3">
        <Col md={6}>
          <Card className="p-3">
            <h5>Your Wishlist</h5>
            <p className="display-6 mb-0">{data.wishlist_count}</p>
          </Card>
        </Col>
        <Col md={6}>
          <Card className="p-3">
            <h5>Compared Products</h5>
            <p className="display-6 mb-0">{data.compared_products}</p>
          </Card>
        </Col>
      </Row>
      <Card className="p-3 mt-4">
        <h5 className="mb-3">Edit Profile</h5>
        {status.error && <Alert variant="danger">{status.error}</Alert>}
        {status.success && <Alert variant="success">{status.success}</Alert>}
        <Form onSubmit={handleUpdateProfile}>
          <Row className="g-3">
            <Col md={6}>
              <Form.Label>First Name</Form.Label>
              <Form.Control
                value={profile.first_name}
                required
                onChange={(e) => setProfile((prev) => ({ ...prev, first_name: e.target.value }))}
              />
            </Col>
            <Col md={6}>
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                value={profile.last_name}
                required
                onChange={(e) => setProfile((prev) => ({ ...prev, last_name: e.target.value }))}
              />
            </Col>
            <Col md={6}>
              <Form.Label>Username</Form.Label>
              <Form.Control
                value={profile.username}
                required
                onChange={(e) => setProfile((prev) => ({ ...prev, username: e.target.value }))}
              />
            </Col>
            <Col md={6}>
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                value={profile.email}
                required
                onChange={(e) => setProfile((prev) => ({ ...prev, email: e.target.value }))}
              />
            </Col>
            <Col md={12}>
              <Form.Label>New Password (optional)</Form.Label>
              <div className="d-flex gap-2">
                <Form.Control
                  type={showNewPassword ? "text" : "password"}
                  value={profile.new_password}
                  minLength={8}
                  placeholder="Leave blank to keep current password"
                  autoComplete="new-password"
                  onChange={(e) => setProfile((prev) => ({ ...prev, new_password: e.target.value }))}
                />
                <Button variant="outline-secondary" type="button" onClick={() => setShowNewPassword((prev) => !prev)}>
                  {showNewPassword ? "Hide" : "Show"}
                </Button>
              </div>
              <Form.Text className="text-muted">
                Use 8+ chars with uppercase, lowercase, number, and special character.
              </Form.Text>
            </Col>
            <Col md={12}>
              <Form.Label>Confirm Password</Form.Label>
              <div className="d-flex gap-2">
                <Form.Control
                  type={showConfirmPassword ? "text" : "password"}
                  value={profile.confirm_password}
                  minLength={8}
                  placeholder="Confirm new password"
                  autoComplete="new-password"
                  onChange={(e) => setProfile((prev) => ({ ...prev, confirm_password: e.target.value }))}
                />
                <Button variant="outline-secondary" type="button" onClick={() => setShowConfirmPassword((prev) => !prev)}>
                  {showConfirmPassword ? "Hide" : "Show"}
                </Button>
              </div>
            </Col>
            <Col md={12}>
              <Button type="submit">Save Changes</Button>
            </Col>
          </Row>
        </Form>
      </Card>
    </>
  );
}
