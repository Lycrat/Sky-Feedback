import React from "react";
import { render, screen } from "@testing-library/react";
import { Layout } from "..";
import { MemoryRouter, Routes, Route } from "react-router";

test("renders navbar and footer with a main class that houses outlet (children)", () => {
  render(
    <MemoryRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="/test" element={<h1>hi</h1>} />
        </Route>
      </Routes>
    </MemoryRouter>
  );
  expect(screen.getByTestId("navbar")).toBeInTheDocument();

  expect(screen.getByRole("main")).toBeInTheDocument();

  expect(screen.getByTestId("footer")).toBeInTheDocument();
});
