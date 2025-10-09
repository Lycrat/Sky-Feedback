import React from "react";
import { Navbar, Footer } from "./";
import { Outlet } from "react-router";
const Layout = () => {
  return (
    <div className="w-full h-auto">
      <Navbar />
      <main className="pt-20 w-full h-full">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
