import { useEffect, useState } from "react";
import { Alert, Card, Spinner } from "react-bootstrap";
import { Link, useSearchParams } from "react-router-dom";
import api from "../api";

export default function VerifyEmailPage() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState({ loading: true, message: "", variant: "info" });

  useEffect(() => {
    const token = searchParams.get("token");
    if (!token) {
      setStatus({ loading: false, message: "Missing verification token in the link.", variant: "danger" });
      return;
    }
    api
      .get(`/auth/verify-email/?token=${encodeURIComponent(token)}`)
      .then((res) => {
        setStatus({ loading: false, message: res.data.detail || "Email verified.", variant: "success" });
      })
      .catch((err) => {
        const msg = err.response?.data?.detail || "Verification failed.";
        setStatus({ loading: false, message: msg, variant: "danger" });
      });
  }, [searchParams]);

  return (
    <Card className="mx-auto auth-card">
      <Card.Body>
        <h3 className="mb-3">Email verification</h3>
        {status.loading ? (
          <div className="d-flex align-items-center gap-2">
            <Spinner animation="border" size="sm" />
            <span>Verifying your email…</span>
          </div>
        ) : (
          <Alert variant={status.variant}>{status.message}</Alert>
        )}
        <p className="mb-0 mt-3">
          <Link to="/login">Go to login</Link>
        </p>
      </Card.Body>
    </Card>
  );
}
