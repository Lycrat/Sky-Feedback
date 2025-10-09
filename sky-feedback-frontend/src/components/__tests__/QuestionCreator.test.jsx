import React from "react";
import { render, screen, fireEvent, within } from "@testing-library/react";
import "@testing-library/jest-dom";
import { QuestionCreator } from "../QuestionCreator";

describe("QuestionCreator", () => {
  test("renders initial question", () => {
    render(<QuestionCreator />);
    expect(screen.getByLabelText(/Question 1/i)).toBeInTheDocument();
  });

  test("adds and removes a question", () => {
    render(<QuestionCreator />);
    fireEvent.click(screen.getByRole("button", { name: /add/i }));
    expect(screen.getAllByLabelText(/Question/i)).toHaveLength(2);

    fireEvent.click(screen.getAllByLabelText(/delete/i)[0]);
    expect(screen.queryAllByLabelText(/Question/i)).toHaveLength(1);
  });

  test("switches to multiple choice and adds option", () => {
    render(<QuestionCreator />);
    fireEvent.mouseDown(screen.getByLabelText(/Answer Type/i));
    fireEvent.click(
      within(screen.getByRole("listbox")).getByText(/Multiple Choice/i)
    );

    const addOption = screen.getByRole("button", { name: /add option/i });
    fireEvent.click(addOption);
    expect(screen.getByPlaceholderText(/Option 1/i)).toBeInTheDocument();
  });

  test("updates question and option text", () => {
    render(<QuestionCreator />);
    const question = screen.getByLabelText(/Question 1/i);
    fireEvent.change(question, { target: { value: "Favorite color?" } });
    expect(question.value).toBe("Favorite color?");

    fireEvent.mouseDown(screen.getByLabelText(/Answer Type/i));
    fireEvent.click(
      within(screen.getByRole("listbox")).getByText(/Multiple Choice/i)
    );
    fireEvent.click(screen.getByRole("button", { name: /add option/i }));

    const option = screen.getByPlaceholderText(/Option 1/i);
    fireEvent.change(option, { target: { value: "Blue" } });
    expect(option.value).toBe("Blue");
  });
});
