import React from "react";
import { Navbar, Footer } from "./";
import { Outlet } from "react-router";
const Layout = () => {
  return (
    <div className="flex flex-col w-full min-h-screen">
      <Navbar />
      <main
        className="pt-30 w-full h-full flex-grow bg-white overflow-scroll md:px-10 lg:px-20"
        role="main div"
      >
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
