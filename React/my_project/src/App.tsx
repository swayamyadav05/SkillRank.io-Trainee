import React, { useState, useEffect } from "react";
import Header from "./components/Header/Header";
import UserTable from "./components/UserTable/UserTable";
import "./App.css";

const App: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]); // State to hold users data
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination states
  const [page, setPage] = useState<number>(1);
  const [limit, setLimit] = useState<number>(20); // Adjust as needed
  const [total, setTotal] = useState<number>(0);

  const fetchData = async (currentPage: number, currentLimit: number) => {
    try {
      const apiUrl = `https://udj5ss8nhe.execute-api.us-east-1.amazonaws.com/default/api/data?page=${currentPage}&limit=${currentLimit}`;
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
    fetchData(page, limit);
  }, [page, limit]);

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

  if (loading) return <div className="loader">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="app-container">
      <Header />
      <UserTable users={users} fetchData={() => fetchData(page, limit)} />
      <div className="pagination">
        <button onClick={handlePreviousPage} disabled={page === 1}>
          Previous
        </button>
        <span>
          Page {page} of {Math.ceil(total / limit)}
        </span>
        <button onClick={handleNextPage} disabled={page * limit >= total}>
          Next
        </button>
      </div>
    </div>
  );
};

export default App;
