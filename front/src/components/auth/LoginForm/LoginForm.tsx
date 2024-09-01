import { useForm, type SubmitHandler } from "react-hook-form";
import type { FormInput } from "./LoginForm.types";
import Input from "../../Input/Input";
import Button from "../../Button/Button";

const LoginForm = () => {
  const { register, handleSubmit } = useForm<FormInput>();
  const onSubmit: SubmitHandler<FormInput> = (data) => console.log(data);

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
      <Button className="mt-4" type="submit">
        Log in
      </Button>
    </form>
  );
};

export default LoginForm;
