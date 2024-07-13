import { useForm } from "react-hook-form";
import type { FormInput } from "./SignupForm.types";
import type { SubmitHandler } from "react-hook-form";
import Input from "../Input/Input";

const SignupForm = () => {
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
      <Input<FormInput>
        label="Confirm password"
        type="password"
        register={register}
        required
      />
      <button type="submit">Sign Up</button>
    </form>
  );
};

export default SignupForm;
