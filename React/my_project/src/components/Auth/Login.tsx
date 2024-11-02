import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Auth.css";

interface LoginProps {
  onLogin: () => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
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
        "https://qublrgg2p0.execute-api.us-east-1.amazonaws.com/default/login",
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

      // Check if the response is ok
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error data:", errorData); // Log the error data
        setError(
          errorData.error || "Login failed. Check credentials or try again."
        );
        return;
      }

      const data = await response.json();

      console.log("Server response:", data);

      if (data.body) {
        let responseBody;
        try {
          responseBody = JSON.parse(data.body);
        } catch (error) {
          console.error("Error parsing response body:", error);
          setError("Failed to parse server response.");
          return;
        }

        console.log("Parsed response body:", responseBody);

        if (responseBody.message === "Login successful !!") {
          onLogin();
          console.log("User logged in successfully.");
          navigate("/home");
        } else {
          setError(
            responseBody.error ||
              "Login failed. Check credentials or try again."
          );
        }
      } else {
        setError("Unexpected response format.");
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
        <div className="password-input-container">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <span
            className="toggle-password"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? "👁️" : "👁️‍🗨️"}
          </span>
        </div>
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <a href="/signup">Sign up here</a>.
      </p>
    </div>
  );
};

export default Login;
