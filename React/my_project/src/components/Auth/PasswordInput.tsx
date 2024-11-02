// PasswordInput.tsx
import React from "react";

interface PasswordInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  showPassword: boolean;
  togglePasswordVisibility: () => void;
  placeholder: string;
}

const PasswordInput: React.FC<PasswordInputProps> = ({
  value,
  onChange,
  showPassword,
  togglePasswordVisibility,
  placeholder,
}) => {
  return (
    <div className="password-input-container">
      <input
        type={showPassword ? "text" : "password"}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required
      />
      <span className="toggle-password" onClick={togglePasswordVisibility}>
        {showPassword ? "👁️" : "👁️‍🗨️"}
      </span>
    </div>
  );
};

export default PasswordInput;
