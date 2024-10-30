import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Auth.css";
import Header from "../Header/Header";

interface LoginProps {
  onLogin: () => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const validateForm = () => {
    if (!username || !password) {
      setError("Username and password are required.");
      return false;
    }
    setError(null);
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const response = await fetch(
        "https://acajyyje6f.execute-api.us-east-1.amazonaws.com/stage1/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            action: "login",
            username,
            password,
          }),
        }
      );

      const data = await response.json(); // Parse response
      console.log("Server response:", data); // Log full response

      // Extract message from the body
      const responseBody = JSON.parse(data.body);
      console.log("Parsed response body:", responseBody); // Log the parsed body

      if (response.ok && responseBody.message === "Login successful !!") {
        onLogin();
        console.log("User logged in successfully.");
        navigate("/home");
      } else {
        setError(
          responseBody.error || "Login failed. Check credentials or try again."
        );
      }
    } catch (error: any) {
      setError("An error occurred. Please try again.");
      console.error("Error during login:", error);
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <a href="/signup">Sign up here</a>.
      </p>
    </div>
  );
};

export default Login;
