// Spinner.tsx
import React from "react";
import "./Spinner.css";

const Spinner: React.FC = () => (
  <div className="spinner-container">
    <div className="spinner">
      <div className="double-bounce1"></div>
      <div className="double-bounce2"></div>
    </div>
  </div>
);

export default Spinner;
