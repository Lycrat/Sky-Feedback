import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  FormControl,
  InputLabel,
  CircularProgress,
  Select,
  MenuItem,
} from "@mui/material";
import { useParams } from "react-router";

export const ViewData = () => {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userList, setUserList] = useState([]);
  const [selectedUser, setSelectedUser] = useState({ id: "", name: "" });

  const { formId } = useParams();

  useEffect(() => {
    const handleFetchAllUsers = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/user/`);
        if (response.status === 200) {
          const data = response.data;
          setUserList(data);
          if (data.length > 0) {
            const firstUser = { id: data[0].id, name: data[0].name };
            setSelectedUser(firstUser);
          }
        } else {
          console.error("Unsuccessful user fetch");
        }
      } catch (err) {
        console.error("Error fetching users:", err);
      }
    };
    handleFetchAllUsers();
  }, []);

  useEffect(() => {
    const handleFetchFormQuestions = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/questionnaire/${formId}/question`
        );
        if (response.status === 200) {
          setQuestions(response.data);
        } else {
          console.error("Request was unsuccessful");
        }
      } catch (err) {
        console.error("Error fetching questions:", err);
      }
    };
    handleFetchFormQuestions();
  }, [formId]);

  useEffect(() => {
    if (!selectedUser?.id || questions.length === 0) return;

    const fetchAllFeedbacks = async () => {
      setLoading(true);
      try {
        const results = await Promise.all(
          questions.map(async (q) => {
            const res = await axios.get(
              `http://localhost:5000/api/questionnaire/${formId}/question/${q.questionnaire_id}/feedback`
            );
            if (res.status === 200) {
              const filtered = res.data.filter(
                (f) => f.userId === selectedUser.id
              );
              return { questionId: q.id, feedback: filtered };
            }
            return null;
          })
        );

        const cleanResults = results.filter((r) => Boolean(r));
        setAnswers(cleanResults);
      } catch (err) {
        console.error("Error fetching feedback:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAllFeedbacks();
  }, [selectedUser, questions, formId]);

  const handleUserSelection = (event) => {
    const name = event.target.value;
    const user = userList.find((u) => u.name === name);
    if (user) setSelectedUser(user);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center -mt-40 w-full h-full bg-gray-100">
        <CircularProgress />
      </div>
    );
  }

  if (!questions || questions.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center -mt-40 w-full h-full gap-2 bg-gray-100">
        <h6 className="text-gray-900">No data found.</h6>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gray-100 px-20 pt-20">
      {console.log("questions", questions)}
      {console.log("answers", answers)}
      <div className="flex flex-row justify-between items-center text-gray-900">
        <h2 className="text-2xl">Form Title</h2>
        <FormControl
          size="large"
          variant="outlined"
          sx={{
            minWidth: 220,
          }}
        >
          <InputLabel id="user-select-label">Selected User</InputLabel>
          <Select
            labelId="user-select-label"
            id="user-select"
            value={selectedUser?.name || ""}
            label="Selected User"
            onChange={handleUserSelection}
          >
            {userList &&
              userList.length > 0 &&
              userList.map((u) => {
                return (
                  <MenuItem key={u.id} value={u.name}>
                    {u.name}
                  </MenuItem>
                );
              })}
          </Select>
        </FormControl>
      </div>

      <div className="flex mt-10 w-full h-screen text-gray-900">
        {questions &&
          questions.map((d, index) => {
            const answerObj = answers.find((a) => a.questionId === d.id);
            const userFeedback =
              answerObj && answerObj.feedback.length > 0
                ? answerObj.feedback[0].feedback
                : "No feedback yet";

            return (
              <div key={index}>
                <h2 className="text-gray-500 font-bold text-2xl">
                  {d.question}
                </h2>
                <h3 className="text-gray-500 font-light text-xl">
                  {userFeedback}
                </h3>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default ViewData;
