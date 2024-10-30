import "./Header.css";
import logo from "../../assets/logo_black.svg";
import React from "react";

interface HeaderProps {
  showLogoutButton: boolean;
  onLogout?: () => void;
}

const Header: React.FC<HeaderProps> = ({ showLogoutButton, onLogout }) => {
  return (
    <header className="header">
      <img src={logo} alt="Logo" className="logo" />
      <div className="header-right">
        {showLogoutButton && (
          <button className="logout-btn" onClick={onLogout}>
            Logout
          </button>
        )}
      </div>
    </header>
  );
};

export default Header;
