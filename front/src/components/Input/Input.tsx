import type { FieldValues } from "react-hook-form";
import type { InputProps } from "./Input.types";

const Input = <T extends FieldValues>({
  label,
  type = "text",
  register,
  required,
}: InputProps<T>) => {
  return (
    <input
      className="my-1"
      type={type}
      {...register(label, { required })}
      placeholder={label}
      aria-label={label}
    />
  );
};

export default Input;
