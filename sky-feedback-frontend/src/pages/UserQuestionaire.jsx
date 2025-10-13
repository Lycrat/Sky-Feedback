import React, { useEffect, useState, Fragment } from "react";
import { useParams } from "react-router";
import axios from "axios";
import { useNavigate } from "react-router";

const TextInput = ({ label, placeholder = "e.g. mrRobot", name, value }) => {
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
        value={value}
      />
    </>
  );
};

const UserQuestionaire = () => {
  const [answers, setAnswers] = useState([]);
  const { id } = useParams();
  const [questions, setQuestions] = useState();
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

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

  const handleChange = (value, dataId) => {
    setAnswers((prev) => {
      const exists = prev.some((ans) => (ans ? ans.id === dataId : false));
      if (exists) {
        return prev.map((ans) =>
          ans.id === dataId ? { ...ans, feedback: value } : ans
        );
      } else {
        return [...prev, { id: dataId, feedback: value }];
      }
    });
  };

  const onSubmit = async (e) => {
    e.preventDefault();

    setIsLoading(true);
    const username = e.target.username.value;
    const name = e.target.name.value;

    let user_id = null;
    // find user id
    try {
      const res = await axios.get("http://localhost:5000/api/user/", {
        params: {
          username: username,
          name: name,
        },
      });
      if (res.data) {
        user_id = res.data[0].id;
      }
    } catch (err) {
      console.log(err);
    }

    // Send feedbacks
    answers.map(async (answer, index) => {
      try {
        const res = await axios.post(
          `http://localhost:5000/api/questionnaire/${id}/question/${answer.id}/feedback`,
          {
            user_id: user_id,
            feedback: answer.feedback,
          }
        );
      } catch (err) {
        console.log(err);
      } finally {
        setIsLoading(false);
      }
    });

    navigate("/");
  };

  const getStoredAnswer = (id) => {
    const answer = answers.find((answer) => answer.id === id);
    return answer ? answer.feedback : "";
  };

  return (
    <div className="flex w-full h-full flex-col bg-white text-black justify-center items-center md:justify-start md:items-start">
      <form
        className="w-full h-full flex flex-col gap-10 lg:w-1/2 p-5"
        onSubmit={onSubmit}
      >
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
              <p className="font-bold text-gray-500 text-2xl">
                {item.question}
              </p>
              {item.type === "multiple" ? (
                <div className="flex flex-col px-5">
                  {item.options.map((label, idx) => {
                    return (
                      <div key={idx}>
                        <label className="flex flex-row gap-3">
                          <input
                            type="radio"
                            value={label}
                            name={`question-${id}`}
                            onChange={(e) =>
                              handleChange(e.target.value, item.id)
                            }
                          />
                          {label}
                        </label>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <textarea
                  type="text"
                  name="answer"
                  className="h-40 md:h-20 lg:h-60 border border-gray-300 rounded-sm p-5 "
                  value={getStoredAnswer(item.id)}
                  onChange={(e) => handleChange(e.target.value, item.id)}
                />
              )}
            </Fragment>
          );
        })}
        <div className="flex flex-col justify-center items-center md:justify-start md:items-start">
          <button
            type="submit"
            className="rounded-lg bg-green-500 w-50 text-white h-10"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

export default UserQuestionaire;
