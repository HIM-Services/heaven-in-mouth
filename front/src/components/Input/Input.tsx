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
      className="py-3 pl-4 my-1 bg-gray-100 rounded-md"
      type={type}
      {...register(label, { required })}
      placeholder={label}
      aria-label={label}
    />
  );
};

export default Input;
