import type { ButtonProps } from "./Button.types";
import "./Button.css";

const Button = ({
  variant = "primary",
  className,
  children,
  ...props
}: ButtonProps) => {
  const buttonClasses = `button-${variant}`;
  return (
    <button className={`${buttonClasses} ${className}`} {...props}>
      {children}
    </button>
  );
};

export default Button;
