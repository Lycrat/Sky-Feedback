import React from "react";
import skyLogo from "../../public/sky-logo.png";
import { useNavigate } from "react-router";
const Navbar = () => {
  const navigate = useNavigate();
  return (
    <div
      data-testid="navbar"
      className="fixed fixed w-full max-h-20 flex justify-center items-center p-5 bg-white shadow-lg  border-1 border-gray-300 z-100"
    >
      <img
        src={skyLogo}
        onClick={() => navigate("/")}
        className="h-full w-20"
      />
    </div>
  );
};

export default Navbar;
