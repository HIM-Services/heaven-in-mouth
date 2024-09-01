import { useForm } from "react-hook-form";
import type { FormInput } from "./SignupForm.types";
import type { SubmitHandler } from "react-hook-form";
import Input from "../../Input/Input";
import Button from "../../Button/Button";

const SignupForm = () => {
  const { register, handleSubmit } = useForm<FormInput>();
  const onSubmit: SubmitHandler<FormInput> = async (data) => {
    console.log(data);
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex flex-col w-full gap-2"
    >
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
      <Button type="submit" className="mt-2">
        Sign Up
      </Button>
    </form>
  );
};

export default SignupForm;
