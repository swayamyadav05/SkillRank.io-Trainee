import "./Header.css";
import logo from "../../assets/logo_black.svg";

const Header: React.FC = () => {
  return (
    <header className="header">
      <img src={logo} alt="Logo" className="logo" />
      <div className="header-right">
        <button className="logout-btn">Logout</button>
      </div>
    </header>
  );
};

export default Header;
