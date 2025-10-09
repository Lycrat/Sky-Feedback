import React, { useEffect, useState, Fragment } from "react";
import { useParams } from "react-router";
import axios from "axios";
const UserQuestionaire = () => {
  const [answers, setAnswers] = useState({});
  const { id } = useParams();
  const [questions, setQuestions] = useState();
  const dummyData = {
    title: "Bamjam",
    questions: [
      {
        title: "How was your overall experience",
      },
    ],
  };

  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/questionnaire/${id}`)
      .then((response) => {
        setQuestions(response.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [answers]);

  useEffect(() => {
    console.log(questions);
  }, [questions]);

  const handleChange = (id, value) => {
    setAnswers((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const onSubmit = (e) => {
    e.preventDefault();
  };

  const TextInput = ({ label, placeholder = "e.g. mrRobot", name }) => {
    return (
      <>
        <label className="font-bold text-gray-500 text-2xl" for="username">
          {label}
        </label>
        <input
          className="border border-gray-300 rounded-sm h-10 pl-5"
          type="text"
          placeholder={placeholder}
          name={name}
        />
      </>
    );
  };
  return (
    <div className="flex w-full h-full flex-col bg-white text-black justify-center items-center md:justify-start md:items-start">
      <form className="w-full h-full flex flex-col gap-10 lg:w-1/2 p-5">
        <p className="text-4xl font-light">
          {" "}
          {questions?.questionnaire[0].title}{" "}
        </p>
        <div className="flex flex-col gap-5 w-full md:w-1/2">
          <TextInput label="Username" name="username" />
          <TextInput label="Name" placeholder="e.g. bryan" name="name" />
        </div>
        {questions?.questions.map((item, index) => {
          return (
            <Fragment key={index}>
              <p className="font-bold text-gray-500 text-2xl">{item.title}</p>
              <textarea
                type="text"
                name="answer"
                className="h-40 md:h-20 lg:h-60 border border-gray-300 rounded-sm p-5 "
                onChange={(e) => handleChange(index, e.target.value)}
              />
            </Fragment>
          );
        })}
      </form>
    </div>
  );
};

export default UserQuestionaire;
