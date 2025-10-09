import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import axios from "axios";
import { ViewData } from "../../pages/ViewData";

jest.mock("axios");

describe("ViewData", () => {
  const mockData = [{ question: "how are you?", answer: "fine mate and you" }];

  beforeEach(() => jest.clearAllMocks());

  test("displays fetched data after loading", async () => {
    axios.get.mockResolvedValueOnce({ status: 200, data: mockData });
    render(<ViewData id="1" userId="2" />);

    await waitFor(() =>
      expect(screen.getByText("how are you?")).toBeInTheDocument()
    );
    expect(screen.getByText("fine mate and you")).toBeInTheDocument();
    expect(screen.getByText("Form Title")).toBeInTheDocument();
  });

  test("shows 'No data found' when no data returned", async () => {
    axios.get.mockResolvedValueOnce({ status: 200, data: null });
    render(<ViewData id="1" userId="2" />);

    await waitFor(() =>
      expect(screen.getByText(/No data found/i)).toBeInTheDocument()
    );
  });

  test("changes selected user", async () => {
    axios.get.mockResolvedValueOnce({ status: 200, data: mockData });
    render(<ViewData id="1" userId="2" />);

    await waitFor(() => screen.getByText("how are you?"));
    const select = screen.getByLabelText(/Selected User/i);
    fireEvent.mouseDown(select);
    fireEvent.click(screen.getByText("Maks"));
    expect(select).toHaveTextContent("Maks");
  });
});
