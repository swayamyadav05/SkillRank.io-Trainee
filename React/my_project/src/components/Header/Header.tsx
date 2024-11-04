import "./Header.css";
import logo from "../../assets/logo_black.svg";
import React from "react";
import { useNavigate } from "react-router-dom";

interface HeaderProps {
  showLogoutButton: boolean;
  onLogout?: () => void;
}

const Header: React.FC<HeaderProps> = ({ showLogoutButton, onLogout }) => {
  const navigate = useNavigate();

  return (
    <header className="header">
      <img
        src={logo}
        alt="Logo"
        className="logo"
        onClick={() => navigate("/home")}
        role="button"
        tabIndex={0}
        aria-label="Navigate to home page"
        onKeyDown={(e) => e.key === "Enter" && navigate("/home")}
      />
      <div className="header-right">
        {showLogoutButton && (
          <button className="logout-btn" onClick={onLogout} aria-label="Logout">
            Logout
          </button>
        )}
      </div>
    </header>
  );
};

export default Header;
