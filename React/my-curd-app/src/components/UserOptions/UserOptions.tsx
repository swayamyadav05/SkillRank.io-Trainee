import React from "react";
import "./UserOptions.css";

interface UserOptionsProps {
  userId: string;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}

const UserOptions: React.FC<UserOptionsProps> = ({
  userId,
  onEdit,
  onDelete,
}) => {
  return (
    <div className="options-dropdown">
      <div className="options-dropdown-arrow"></div>
      <ul>
        <li onClick={() => onEdit(userId)}>Edit</li>
        <li onClick={() => onDelete(userId)}>Delete</li>
      </ul>
    </div>
  );
};

export default UserOptions;
