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
import DataRow from "../components/DataRow";

export const ViewData = () => {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userList, setUserList] = useState([]);
  const [formTitle, setFormTitle] = useState("");
  const [selectedUser, setSelectedUser] = useState({ id: "", name: "" });

  const { formId } = useParams();

  useEffect(() => {
    const handleFetchTitle = async () => {
      try {
        const res = await axios.get(
          `http://localhost:5000/api/questionnaire/${formId}`
        );
        if (res.status == 200) {
          console.log("res", res);
          setFormTitle(res.data.questionnaire[0].title);
        } else {
          console.error("Unable to fetch form title");
        }
      } catch (err) {
        console.log(err);
      }
    };

    handleFetchTitle();

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
              `http://localhost:5000/api/questionnaire/${formId}/question/${q.id}/feedback`
            );
            if (res.status === 200) {
              console.log(res.data);
              const filtered = res.data.filter(
                (f) => f.user_id === selectedUser.id
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

  return (
    <div className="flex flex-col h-full bg-gray-100 px-20 pt-20">
      {/* {console.log("questions", questions)}
      {console.log("answers", answers)} */}
      {console.log(userList)}
      <div className="flex flex-row justify-between items-center text-gray-900">
        <h2 className="text-2xl">{formTitle ? formTitle : "Form Title"}</h2>
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

      <div className="flex flex-col gap-14 mt-10 w-full h-screen text-gray-900">
        {questions &&
          questions.map((d, index) => {
            console.log("answers", answers);
            const answerObj = answers.find((a) => a.questionId === d.id);
            // console.log(answerObj);

            return (
              <DataRow
                key={index}
                answerObj={answerObj}
                question={d.question}
              />
            );
          })}
      </div>
    </div>
  );
};

export default ViewData;
