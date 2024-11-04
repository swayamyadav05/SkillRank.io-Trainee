import React from "react";

interface PasswordInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  showPassword: boolean;
  togglePasswordVisibility: () => void;
  placeholder: string;
  id: string;
}

const PasswordInput: React.FC<PasswordInputProps> = ({
  value,
  onChange,
  showPassword,
  togglePasswordVisibility,
  placeholder,
  id,
}) => {
  return (
    <div className="password-input-container">
      <input
        type={showPassword ? "text" : "password"}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required
        aria-label={placeholder}
        id={id}
        className="password-input"
      />
      <span
        className="toggle-password"
        onClick={togglePasswordVisibility}
        onKeyDown={(e) => e.key === "Enter" && togglePasswordVisibility()}
        role="button"
        tabIndex={0}
        aria-label={showPassword ? "Hide password" : "Show password"}
      >
        {showPassword ? "👁️" : "👁️‍🗨️"}
      </span>
    </div>
  );
};

export default PasswordInput;
