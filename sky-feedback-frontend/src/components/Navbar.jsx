import React from "react";
import skyLogo from "../../public/sky-logo.png";
const Navbar = () => {
  return (
    <div
      data-testid="navbar"
      className="w-full max-h-20 flex justify-center items-center p-5 bg-white shadow-lg border-1"
    >
      <img src={skyLogo} className="h-full w-20" />
    </div>
  );
};

export default Navbar;
