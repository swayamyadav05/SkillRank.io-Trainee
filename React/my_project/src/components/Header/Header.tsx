import "./Header.css";
import logo from "../../assets/logo_black.svg";
import React from "react";
import { Link } from "react-router-dom";

interface HeaderProps {
  showLogoutButton: boolean;
}

const Header: React.FC<HeaderProps> = ({ showLogoutButton }) => {
  return (
    <header className="header">
      <img src={logo} alt="Logo" className="logo" />
      <div className="header-right">
        {showLogoutButton && <button className="logout-btn">Logout</button>}
      </div>
    </header>
  );
};

export default Header;
