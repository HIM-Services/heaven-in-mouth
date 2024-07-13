import logo from "../../assets/logo.svg";

const Navbar = () => {
  return (
    <nav className="sticky h-16 flex items-center px-4 border-b-gray-200 border">
      <img src={logo.src} alt="logo" />
    </nav>
  );
};

export default Navbar;
