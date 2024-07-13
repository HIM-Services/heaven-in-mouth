import type { UseFormRegister, FieldValues, Path } from "react-hook-form";

export interface InputProps<T extends FieldValues> {
  label: Path<T>;
  type: "number" | "text" | "password" | "email";
  register: UseFormRegister<T>;
  required: boolean;
}
