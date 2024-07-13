import { useForm, type SubmitHandler } from "react-hook-form";
import type { FormInput } from "./LoginForm.types";
import Input from "../Input/Input";

const LoginForm = () => {
  const { register, handleSubmit } = useForm<FormInput>();
  const onSubmit: SubmitHandler<FormInput> = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col">
      <Input<FormInput>
        label="Email"
        type="email"
        register={register}
        required
      />
      <Input<FormInput>
        label="Password"
        type="password"
        register={register}
        required
      />
      <button type="submit">Sign Up</button>
    </form>
  );
};

export default LoginForm;
