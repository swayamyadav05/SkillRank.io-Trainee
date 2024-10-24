import React, { useState, useEffect } from "react";
import "./UserTable.css";
import UserOptions from "../UserOptions/UserOptions";
import UserFormModal from "../UserFormModal/UserFormModal";
import {
  fetchUsers,
  createUser,
  updateUser,
  deleteUser,
} from "../../api/LambdaIntegration";

interface User {
  _id: string;
  name: string;
  language: string;
  id: string;
  bio: string;
  version: number;
}

interface UserTableProps {
  users: User[];
  fetchData: () => void;
}

const UserTable: React.FC<UserTableProps> = ({ users, fetchData }) => {
  const [showOptions, setShowOptions] = useState<{ [key: string]: boolean }>(
    {}
  );
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUsers();
  }, [fetchData]);

  const toggleOptions = (id: string) => {
    setShowOptions((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const handleEdit = (id: string) => {
    const userToEdit = users.find((user) => user._id === id);
    setEditingUser(userToEdit || null);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    setLoading(true);
    try {
      await deleteUser(id);
      fetchData();
    } catch (error) {
      setError("Error deleting user.");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = () => {
    setEditingUser(null);
    setIsModalOpen(true);
  };

  const handleFormSubmit = async (formData: User) => {
    setLoading(true);
    try {
      const { _id, ...updateData } = formData;

      if (editingUser) {
        await updateUser(editingUser._id, updateData);
      } else {
        await createUser(formData);
      }
      await fetchData();
    } catch (error) {
      setError("Error submitting form.");
    } finally {
      setLoading(false);
      setIsModalOpen(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="table-container">
      <div className="table-header">
        <h2>User Table</h2>
        <button className="create-user-btn" onClick={handleCreateUser}>
          Create User
        </button>
      </div>
      <table className="user-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Language</th>
            <th>ID</th>
            <th>Bio</th>
            <th>Version</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {Array.isArray(users) && users.length > 0 ? (
            users.map((user) => (
              <tr key={user._id}>
                <td>{user.name}</td>
                <td>{user.language}</td>
                <td>{user.id}</td>
                <td>{user.bio}</td>
                <td>{user.version}</td>
                <td>
                  <div className="options-container">
                    <button
                      onClick={() => toggleOptions(user._id)}
                      className="options-btn"
                    >
                      ...
                    </button>
                    {showOptions[user._id] && (
                      <UserOptions
                        userId={user._id}
                        onEdit={handleEdit}
                        onDelete={handleDelete}
                      />
                    )}
                  </div>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={6}>No users available</td>
            </tr>
          )}
        </tbody>
      </table>
      <UserFormModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleFormSubmit}
        existingUser={editingUser}
      />
    </div>
  );
};

export default UserTable;
