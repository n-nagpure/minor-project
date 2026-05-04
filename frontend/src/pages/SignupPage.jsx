import { useState } from "react";
import { Alert, Button, Card, Form } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";

export default function SignupPage() {
  const [form, setForm] = useState({ 
    username: "", 
    first_name: "", 
    last_name: "", 
    email: "", 
    password: "", 
    confirm_password: "" 
  });
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const navigate = useNavigate();
  const passwordRuleText = "Min 8 chars, with uppercase, lowercase, number, and special character.";

  const extractErrorMessage = (err) => {
    const data = err?.response?.data;
    if (!data) return "Signup failed. Please try again.";
    if (typeof data === "string") return data;
    if (data.detail) return data.detail;
    const messages = Object.entries(data).flatMap(([field, values]) => {
      const list = Array.isArray(values) ? values : [values];
      return list.map((value) => `${field}: ${value}`);
    });
    return messages.length ? messages.join(" | ") : "Signup failed. Please check your details.";
  };

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    
    // Client-side validation
    if (form.password !== form.confirm_password) {
      setError("confirm_password: Passwords do not match.");
      return;
    }
    
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/;
    if (!passwordPattern.test(form.password)) {
      setError(`password: ${passwordRuleText}`);
      return;
    }
    
    try {
      const res = await api.post("/auth/signup/", form);
      setError("");
      navigate("/login", { state: { signupMessage: res.data?.detail || "Check your email to verify your account." } });
    } catch (err) {
      setError(extractErrorMessage(err));
    }
  };

  return (
    <Card className="mx-auto auth-card">
      <Card.Body>
        <h3 className="mb-3">Sign Up</h3>
        {error && <Alert variant="danger">{error}</Alert>}
        <Form onSubmit={submit}>
          <Form.Group className="mb-3">
            <Form.Label>First Name</Form.Label>
            <Form.Control
              value={form.first_name}
              minLength={1}
              maxLength={30}
              pattern="[A-Za-z\s]+"
              title="Enter your first name (letters and spaces only)"
              placeholder="e.g., John"
              required
              onChange={(e) => setForm({ ...form, first_name: e.target.value })}
            />
            <Form.Text className="text-muted">Enter your first name (letters only)</Form.Text>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Last Name</Form.Label>
            <Form.Control
              value={form.last_name}
              minLength={1}
              maxLength={30}
              pattern="[A-Za-z\s]+"
              title="Enter your last name (letters and spaces only)"
              placeholder="e.g., Doe"
              required
              onChange={(e) => setForm({ ...form, last_name: e.target.value })}
            />
            <Form.Text className="text-muted">Enter your last name (letters only)</Form.Text>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control
              value={form.username}
              minLength={3}
              required
              onChange={(e) => setForm({ ...form, username: e.target.value })}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              value={form.email}
              required
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <div className="d-flex gap-2">
              <Form.Control
                type={showPassword ? "text" : "password"}
                value={form.password}
                minLength={8}
                pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$"
                title={passwordRuleText}
                required
                onChange={(e) => setForm({ ...form, password: e.target.value })}
              />
              <Button variant="outline-secondary" type="button" onClick={() => setShowPassword((prev) => !prev)}>
                {showPassword ? "Hide" : "Show"}
              </Button>
            </div>
            <Form.Text className="text-muted">{passwordRuleText}</Form.Text>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Confirm Password</Form.Label>
            <div className="d-flex gap-2">
              <Form.Control
                type={showConfirmPassword ? "text" : "password"}
                value={form.confirm_password}
                minLength={8}
                required
                onChange={(e) => setForm({ ...form, confirm_password: e.target.value })}
              />
              <Button variant="outline-secondary" type="button" onClick={() => setShowConfirmPassword((prev) => !prev)}>
                {showConfirmPassword ? "Hide" : "Show"}
              </Button>
            </div>
            <Form.Text className="text-muted">Re-enter your password to confirm</Form.Text>
          </Form.Group>
          <Button type="submit" className="w-100">
            Create Account
          </Button>
        </Form>
        <p className="mt-3 mb-0">
          Already registered? <Link to="/login">Login</Link>
        </p>
      </Card.Body>
    </Card>
  );
}
