import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import HomeDashboard from "../HomeDashboard";

// Mock FormCardContainer to isolate HomeDashboard tests
jest.mock("../../components/FormCardContainer", () => jest.fn(() => <div data-testid="form-card-container" />));

describe("HomeDashboard", () => {

  it("renders the heading 'My Forms'", () => {
    render(
      <MemoryRouter>
        <HomeDashboard />
      </MemoryRouter>
    );

    const heading = screen.getByRole("heading", { name: /my forms/i });
    expect(heading).toBeInTheDocument();
  });

  it("renders the FormCardContainer component", () => {
    render(
      <MemoryRouter>
        <HomeDashboard />
      </MemoryRouter>
    );

    const formCardContainer = screen.getByTestId("form-card-container");
    expect(formCardContainer).toBeInTheDocument();
  });
});
