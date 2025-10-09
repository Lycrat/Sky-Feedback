import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import FormCardContainer from "../FormCardContainer";

// Mock navigate
const mockNavigate = jest.fn();
jest.mock("react-router", () => ({
  ...jest.requireActual("react-router"),
  useNavigate: () => mockNavigate,
}));

// Mock FormCard component (we only care that it renders)
jest.mock("../FormCard", () => ({ data }) => (
  <div data-testid="form-card">
    MockFormCard - {data.cardTitle} ({data.questionnaire_id})
  </div>
));

describe("FormCardContainer", () => {
  const mockData = [
    { questionnaire_id: 1, cardTitle: "Survey 1" },
    { questionnaire_id: 2, cardTitle: "Survey 2" },
  ];

  it("renders the correct number of FormCard components", () => {
    render(
      <MemoryRouter>
        <FormCardContainer data={mockData} />
      </MemoryRouter>
    );

    const cards = screen.getAllByTestId("form-card");
    expect(cards).toHaveLength(2);

    // Check that titles are passed correctly
    expect(screen.getByText(/Survey 1/)).toBeInTheDocument();
    expect(screen.getByText(/Survey 2/)).toBeInTheDocument();
  });

  it("renders an 'Add Form' button with a plus sign", () => {
    render(
      <MemoryRouter>
        <FormCardContainer data={mockData} />
      </MemoryRouter>
    );

    const addButton = screen.getByRole("button", { name: "+" });
    expect(addButton).toBeInTheDocument();
  });

  it("calls navigate('/create-form') when 'Add Form' button is clicked", () => {
    render(
      <MemoryRouter>
        <FormCardContainer data={mockData} />
      </MemoryRouter>
    );

    const addButton = screen.getByRole("button", { name: "+" });
    fireEvent.click(addButton);

    expect(mockNavigate).toHaveBeenCalledWith("/create-form");
  });

  it("has correct layout container styling", () => {
    render(
      <MemoryRouter>
        <FormCardContainer data={mockData} />
      </MemoryRouter>
    );

    const gridContainer = screen.getByRole("button", { name: "+" }).parentElement;
    expect(gridContainer).toHaveClass("grid");
    expect(gridContainer).toHaveClass("gap-8");
    expect(gridContainer).toHaveClass("place-items-center");
  });
});
