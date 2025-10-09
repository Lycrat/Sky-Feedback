import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import FormCard from "../FormCard";

const mockNavigate = jest.fn();
jest.mock("react-router", () => ({
  ...jest.requireActual("react-router"),
  useNavigate: () => mockNavigate,
}));

describe("FormCard Component", () => {
  const mockData = {
    questionnaire_id: "123",
    cardTitle: "Customer Feedback Form",
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders the card title correctly", () => {
    render(
      <MemoryRouter>
        <FormCard data={mockData} />
      </MemoryRouter>
    );
    expect(screen.getByText("Customer Feedback Form")).toBeInTheDocument();
    const linkElement = screen.getByRole("link", { name: /customer feedback form/i });
    expect(linkElement).toBeInTheDocument();
    expect(linkElement).toHaveAttribute("href", "/questionnaire/123");
  });

  it("navigates to edit page when Edit button is clicked", () => {
    render(
      <MemoryRouter>
        <FormCard data={mockData} />
      </MemoryRouter>
    );

    const editButton = screen.getByText("Edit");
    fireEvent.click(editButton);

    expect(mockNavigate).toHaveBeenCalledWith("/edit/123");
  });

  it("navigates to answers page when View Answers button is clicked", () => {
    render(
      <MemoryRouter>
        <FormCard data={mockData} />
      </MemoryRouter>
    );

    const viewAnswersButton = screen.getByText("View Answers");
    fireEvent.click(viewAnswersButton);

    expect(mockNavigate).toHaveBeenCalledWith("/answers/123");
  });

  it("renders both Edit and View Answers buttons", () => {
    render(
      <MemoryRouter>
        <FormCard data={mockData} />
      </MemoryRouter>
    );

    expect(screen.getByText("Edit")).toBeInTheDocument();
    expect(screen.getByText("View Answers")).toBeInTheDocument();
  });
});
