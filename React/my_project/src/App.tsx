import React, { useState, useEffect } from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Header from "./components/Header/Header";
import UserTable from "./components/UserTable/UserTable";
import Login from "./components/Auth/Login";
import Signup from "./components/Auth/Signup";
import Spinner from "./components/Spinner/Spinner";
import "./App.css";

const BASE_URL =
  "https://2ccs2nm0l9.execute-api.us-east-1.amazonaws.com/default/api";

const App: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1);
  const [limit, setLimit] = useState<number>(20);
  const [total, setTotal] = useState<number>(0);
  const navigate = useNavigate();

  // Fetch data function with authentication check
  const fetchData = async (currentPage: number, currentLimit: number) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${BASE_URL}/data?page=${currentPage}&limit=${currentLimit}`
      );
      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      const result = await response.json();
      setUsers(result.data);
      setTotal(result.total);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchData(page, limit);
    }
  }, [isAuthenticated, page, limit]);

  const handleNextPage = () => {
    if (page * limit < total) setPage((prev) => prev + 1);
  };

  const handlePreviousPage = () => {
    if (page > 1) setPage((prev) => prev - 1);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUsers([]);
    navigate("/login");
    console.log("User logged out");
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
    navigate("/home");
    console.log("User logged in");
  };

  const handleSignup = () => {
    navigate("/login");
    console.log("User signed up successfully");
  };

  if (loading) {
    return (
      <div className="loader">
        <Spinner />
      </div>
    );
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="app-container">
      <Header showLogoutButton={isAuthenticated} onLogout={handleLogout} />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Navigate to="/signup" replace />} />
          <Route
            path="/home"
            element={
              isAuthenticated ? (
                <UserTable
                  users={users}
                  total={total}
                  page={page}
                  limit={limit}
                  onNextPage={handleNextPage}
                  onPreviousPage={handlePreviousPage}
                  fetchData={() => fetchData(page, limit)}
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/signup" element={<Signup onSignup={handleSignup} />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;
