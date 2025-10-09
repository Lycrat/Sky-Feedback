import React, { useState, useEffect } from "react";
import { TextField, Button, MenuItem, IconButton, Radio } from "@mui/material";
import { Delete, Add } from "@mui/icons-material";

export const QuestionCreator = ({ onQuestionChange }) => {
  const [questions, setQuestions] = useState([
    { id: Date.now(), text: "", type: "textarea", options: [] },
  ]);

    useEffect(() => {
    if (onQuestionChange) {
      onQuestionChange(questions);
    }
  }, [questions]);

  const addQuestion = () => {
    setQuestions((prev) => [
      ...prev,
      { id: Date.now(), text: "", type: "textarea", options: [] },
    ]);
  };

  const updateQuestion = (id, field, value) => {
    setQuestions((prev) =>
      prev.map((q) =>
        q.id === id
          ? {
              ...q,
              [field]: value,
              options: field === "type" && value !== "multiple" ? [] : q.options,
            }
          : q
      )
    );
  };

  const removeQuestion = (id) => {
    setQuestions((prev) => prev.filter((q) => q.id !== id));
  };

  const addOption = (qId) => {
    setQuestions((prev) =>
      prev.map((q) =>
        q.id === qId
          ? { ...q, options: [...q.options, ''] }
          : q
      )
    );
  };

  const updateOption = (qId, index, value) => {
    setQuestions((prev) =>
      prev.map((q) =>
        q.id === qId
          ? {
              ...q,
              options: q.options.map((opt, i) => (i === index ? value : opt)),
            }
          : q
      )
    );
  };

  const removeOption = (qId, index) => {
    setQuestions((prev) =>
      prev.map((q) =>
        q.id === qId
          ? { ...q, options: q.options.filter((_, i) => i !== index) }
          : q
      )
    );
  };

  return (
    <div className="flex justify-center items-center min-h-screen min-w-screen bg-gray-50">
        {console.log(questions)}
      <div className="flex flex-col justify-center items-center w-[80%] bg-gray-100 rounded-2xl p-8 border border-gray-200 overflow-y-auto padding-top-10 padding-bottom-10">

        {!questions ||
          (questions && questions.length < 1 && (
            <h1 className="flex justify-center items-center text-gray-400 !text-base">
              No questions have been added yet.
            </h1>
          ))}

        {questions.map((question, index) => (
          <div key={question.id} className="rounded-xl p-4 mb-4 w-[100%]">
            <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
              <TextField
                label={`Question ${index + 1}`}
                variant="outlined"
                fullWidth
                value={question.text}
                onChange={(e) =>
                  updateQuestion(question.id, "text", e.target.value)
                }
              />

              <TextField
                select
                label="Answer Type"
                value={question.type}
                onChange={(e) =>
                  updateQuestion(question.id, "type", e.target.value)
                }
                className="w-full md:w-48"
              >
                <MenuItem value="textarea">Paragraph</MenuItem>
                <MenuItem value="multiple">Multiple Choice</MenuItem>
              </TextField>

              <IconButton
                color="error"
                onClick={() => removeQuestion(question.id)}
                className="self-center"
              >
                <Delete />
              </IconButton>
            </div>

            {question.type === "multiple" && (
              <div className="mt-4 space-y-3">
                {question.options?.map((option, optIndex) => (
                  <div
                    key={optIndex}
                    className="flex items-center gap-3 rounded-lg p-2"
                  >
                    <Radio disabled />
                    <TextField
                      variant="outlined"
                      placeholder={`Option ${optIndex + 1}`}
                      value={option}
                      onChange={(e) =>
                        updateOption(question.id, optIndex, e.target.value)
                      }
                      className="flex-1"
                    />
                    <IconButton
                      color="error"
                      onClick={() => removeOption(question.id, optIndex)}
                    >
                      <Delete fontSize="small" />
                    </IconButton>
                  </div>
                ))}

                <Button
                  variant="outlined"
                  startIcon={<Add />}
                  onClick={() => addOption(question.id)}
                  className="!rounded-md"
                >
                  Add Option
                </Button>
              </div>
            )}
          </div>
        ))}

        <div className="flex justify-center mt-6">
          <Button
            variant="contained"
            color="primary"
            onClick={addQuestion}
            className="!rounded-md !py-2 !px-6"
          >
            Add
          </Button>
        </div>
      </div>
    </div>
  );
};

export default QuestionCreator;
