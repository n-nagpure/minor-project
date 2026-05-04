import { useEffect, useState } from "react";
import { Alert, Button, Card, Form } from "react-bootstrap";
import { Link, useLocation, useNavigate } from "react-router-dom";
import api from "../api";

export default function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.state?.signupMessage) {
      setInfo(location.state.signupMessage);
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location, navigate]);

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const response = await api.post("/auth/login/", form);
      localStorage.setItem("token", response.data.token);
      localStorage.setItem("username", response.data.username);
      localStorage.setItem("first_name", response.data.first_name || "");
      localStorage.setItem("last_name", response.data.last_name || "");
      navigate("/compare");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Backend may be unreachable.");
    }
  };

  return (
    <Card className="mx-auto auth-card">
      <Card.Body>
        <h3 className="mb-3">Login</h3>
        {info && <Alert variant="success">{info}</Alert>}
        {error && <Alert variant="danger">{error}</Alert>}
        <Form onSubmit={submit}>
          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <div className="d-flex gap-2">
              <Form.Control
                type={showPassword ? "text" : "password"}
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
              />
              <Button variant="outline-secondary" type="button" onClick={() => setShowPassword((prev) => !prev)}>
                {showPassword ? "Hide" : "Show"}
              </Button>
            </div>
          </Form.Group>
          <Button type="submit" className="w-100">
            Login
          </Button>
        </Form>
        <p className="mt-3 mb-0">
          New user? <Link to="/signup">Create account</Link>
        </p>
      </Card.Body>
    </Card>
  );
}
