import { useState } from "react";
import "./Login.css";
const API_URL = "http://127.0.0.1:5000";

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (data.student_id) {
      onLogin(data.student_id);
    } else {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="login-container">
      <h2 className="login-title">Login</h2>

      <input
        className="login-input"
        placeholder="Email"
        onChange={e => setEmail(e.target.value)}
      />

      <input
        className="login-input"
        type="password"
        placeholder="Password"
        onChange={e => setPassword(e.target.value)}
      />

      <button
        className="login-button"
        onClick={handleLogin}
      >
        Login
      </button>
    </div>
  );
}

export default Login;
