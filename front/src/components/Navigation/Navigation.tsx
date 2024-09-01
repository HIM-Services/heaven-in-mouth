import { ShoppingBagIcon } from "@heroicons/react/24/outline";
import logo from "../../assets/logo.svg";
import Button from "../Button/Button";
import { ShoppingCartIcon } from "@heroicons/react/24/outline";
import LocationPicker from "../LocationPicker/LocationPicker";

const Navigation = () => {
  return (
    <>
      <LocationPicker />
      <div className="flex gap-2">
        <Button variant="secondary" className="p-3 rounded-full">
          <ShoppingCartIcon className="size-5" />
        </Button>
        <Button variant="secondary">
          <a href="/auth/login">Log in</a>
        </Button>
        <Button variant="secondary">
          <a href="/auth/signup">Sign up</a>
        </Button>
      </div>
    </>
  );
};

export default Navigation;
