import React, { useState, useEffect, useRef } from "react";
import { TextField, Button, MenuItem, IconButton, Radio } from "@mui/material";
import { Delete, Add } from "@mui/icons-material";

export const QuestionCreator = ({ onQuestionChange, initialQuestions }) => {
  const [questions, setQuestions] = useState([
    { id: Date.now(), question: "", type: "textarea", options: [] },
  ]);
  const hasLoadedInitialData = useRef(false);

  useEffect(() => {
    // Only load initial data once, when it first arrives
    if (initialQuestions && initialQuestions.length > 0 && !hasLoadedInitialData.current) {
      console.log(initialQuestions)
      let formattedQuestions = initialQuestions.map(obj => {
        if (Array.isArray(obj.options) && obj.options.length === 0) {
          return { ...obj, type: "textarea" };
        } else {
          return { ...obj, type: "multiple" };
        }
      });
      setQuestions(formattedQuestions);
      hasLoadedInitialData.current = true;
    }
  }, [initialQuestions]);

  useEffect(() => {
    if (onQuestionChange) {
      onQuestionChange(questions);
    }
  }, [questions]);

  const addQuestion = () => {
    setQuestions((prev) => [
      ...prev,
      { id: Date.now(), question: "", type: "textarea", options: [] },
    ]);
  };

  const updateQuestion = (id, field, value) => {
    setQuestions((prev) =>
      prev.map((q) =>
        q.id === id
          ? {
              ...q,
              [field]: value,
              options:
                field === "type" && value !== "multiple" ? [] : q.options,
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
        q.id === qId ? { ...q, options: [...q.options, ""] } : q
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
      <div className="flex flex-col justify-center items-center w-[80%] bg-white rounded-2xl p-8 shadow-md border border-gray-200 overflow-y-auto padding-top-10 padding-bottom-10">
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
                value={question.question}
                onChange={(e) =>
                  updateQuestion(question.id, "question", e.target.value)
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
                aria-label="delete"
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
                      aria-label="Delete"
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
  );
};

export default QuestionCreator;
