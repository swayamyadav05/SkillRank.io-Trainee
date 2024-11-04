import React, { useState, useEffect } from "react";
import "./UserFormModal.css";

interface UserFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (user: any) => void;
  existingUser?: any;
}

const UserFormModal: React.FC<UserFormModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  existingUser,
}) => {
  const [formData, setFormData] = useState({
    name: "",
    language: "",
    bio: "",
    version: 1.0,
  });

  useEffect(() => {
    if (existingUser) {
      setFormData({
        name: existingUser.name || "",
        language: existingUser.language || "",
        bio: existingUser.bio || "",
        version: existingUser.version || 1.0,
      });
    } else {
      setFormData({
        name: "",
        language: "",
        bio: "",
        version: 1.0,
      });
    }
  }, [existingUser]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (existingUser) {
      onSubmit({ ...existingUser, ...formData });
    } else {
      onSubmit(formData);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal">
      <div className="modal-content">
        <h2 className="form-title">
          {existingUser ? "Edit User" : "Create User"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name:</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label>Language:</label>
            <input
              type="text"
              name="language"
              value={formData.language}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label>Bio:</label>
            <input
              type="text"
              name="bio"
              value={formData.bio}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label>Version:</label>
            <input
              type="number"
              name="version"
              value={formData.version}
              onChange={handleInputChange}
              step="0.1"
            />
          </div>
          <button type="submit">Submit</button>
          <button type="button" onClick={onClose}>
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
};

export default UserFormModal;
