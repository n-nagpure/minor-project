import { useEffect, useState } from "react";
import { Button, Container, Nav, Navbar } from "react-bootstrap";
import { Link, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import ComparePage from "./pages/ComparePage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import VerifyEmailPage from "./pages/VerifyEmailPage";
import WishlistPage from "./pages/WishlistPage";
import api from "./api";
import logo from "../assets/logo.jpeg";

function PrivateRoute({ children }) {
  return localStorage.getItem("token") ? children : <Navigate to="/login" replace />;
}

export default function App() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

  useEffect(() => {
    document.body.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const handleLogout = async () => {
    try {
      await api.post("/auth/logout/");
    } catch (error) {
      // Ignore network failures and clear local token.
    } finally {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("first_name");
      localStorage.removeItem("last_name");
      navigate("/login");
    }
  };

  return (
    <>
      <Navbar variant="dark" expand="lg" className="app-navbar shadow-sm" collapseOnSelect>
        <Container>
          <Navbar.Brand as={Link} to={token ? "/compare" : "/login"} className="navbar-brand-logo">
            <img src={logo} alt="Price Compare" className="navbar-logo" />
            <span className="navbar-text">Price Comparison</span>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="main-navbar" />
          <Navbar.Collapse id="main-navbar">
            <Nav className="ms-auto align-items-center">
              <Button
                variant="outline-light"
                size="sm"
                className="me-2 mt-1 mb-1 mobile-theme-toggle"
                onClick={() => setTheme((prev) => (prev === "light" ? "dark" : "light"))}
              >
                {theme === "light" ? "Dark Mode" : "Light Mode"}
              </Button>
              {token && (
                <>
                  <Nav.Link as={Link} to="/compare">
                    Compare
                  </Nav.Link>
                  <Nav.Link as={Link} to="/dashboard">
                    Dashboard
                  </Nav.Link>
                  <Nav.Link as={Link} to="/wishlist">
                    Wishlist
                  </Nav.Link>
                  <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
                </>
              )}
              {!token && (
                <>
                  <Nav.Link as={Link} to="/login">
                    Login
                  </Nav.Link>
                  <Nav.Link as={Link} to="/signup">
                    Sign Up
                  </Nav.Link>
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="py-4">
        <Routes>
          <Route path="/" element={<Navigate to={token ? "/compare" : "/login"} replace />} />
          <Route path="/login" element={token ? <Navigate to="/compare" replace /> : <LoginPage />} />
          <Route path="/signup" element={token ? <Navigate to="/compare" replace /> : <SignupPage />} />
          <Route path="/verify-email" element={<VerifyEmailPage />} />
          <Route
            path="/compare"
            element={
              <PrivateRoute>
                <ComparePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/wishlist"
            element={
              <PrivateRoute>
                <WishlistPage />
              </PrivateRoute>
            }
          />
          <Route path="*" element={<Navigate to={token ? "/compare" : "/login"} replace />} />
        </Routes>
      </Container>
    </>
  );
}
