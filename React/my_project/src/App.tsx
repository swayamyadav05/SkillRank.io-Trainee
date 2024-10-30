import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Header from "./components/Header/Header";
import UserTable from "./components/UserTable/UserTable";
import Login from "./components/Auth/Login";
import Signup from "./components/Auth/Signup";
import "./App.css";

const BASE_URL =
  "https://2ccs2nm0l9.execute-api.us-east-1.amazonaws.com/default/api";

const App: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1);
  const [limit, setLimit] = useState<number>(20);
  const [total, setTotal] = useState<number>(0);

  const fetchData = async (currentPage: number, currentLimit: number) => {
    try {
      const apiUrl = `${BASE_URL}/data?page=${currentPage}&limit=${currentLimit}`;
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      const result = await response.json();
      setUsers(result.data);
      setTotal(result.total);
      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchData(page, limit);
    } else {
      console.log("User not authenticated, no data fetched.");
      setLoading(false); // Set loading to false if not authenticated to avoid infinite loading state
    }
  }, [isAuthenticated, page, limit]);

  const handleNextPage = () => {
    if (page * limit < total) {
      setPage((prev) => prev + 1);
    }
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage((prev) => prev - 1);
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    console.log("User logged out");
  };

  if (loading) return <div className="loader">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Navigate to="/signup" replace />} />
          <Route
            path="/home"
            element={
              isAuthenticated ? (
                <>
                  <Header showLogoutButton={true} onLogout={handleLogout} />
                  <UserTable
                    users={users}
                    total={total}
                    page={page}
                    limit={limit}
                    onNextPage={handleNextPage}
                    onPreviousPage={handlePreviousPage}
                    fetchData={() => fetchData(page, limit)} // Pass fetchData as a prop
                  />
                </>
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/login"
            element={<Login onLogin={() => setIsAuthenticated(true)} />}
          />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
