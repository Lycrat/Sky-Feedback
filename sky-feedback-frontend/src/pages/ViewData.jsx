import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  FormControl,
  InputLabel,
  CircularProgress,
  Select,
  MenuItem,
} from "@mui/material";

// const apiUrl = import.meta.env.VITE_API_URL;

export const ViewData = ({ id, userId }) => {
  const [data, setData] = useState([
    { question: "how are you?", answer: "fine mate and you" },
  ]);
  const [loading, setLoading] = useState(true);
  const [userList, setUserList] = useState(null);
  const [selectedUser, setSelectedUser] = useState("None");

  useEffect(() => {
    const handleFetchAllUsers = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/user/`);
        if (response.status == 200) {
          console.log("successful");
          console.log(response);
          const data = response.data;
          setUserList(data);
          const firstUser = data[0].name;
          setSelectedUser(firstUser);
        } else {
          console.error("unsuccessful");
        }
      } catch (err) {
        console.error(err);
      }
    };
    handleFetchAllUsers();
  }, []);

  useEffect(() => {
    const handleFetchUserData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5000/${id}/${userId}/`
        );
        if (response.status === 200) {
          setData(response.data);
          console.log("Successful");
        } else {
          console.error("Request was unsuccessful");
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    handleFetchUserData();
  }, [id]);

  const handleUserSelection = (e) => {
    setSelectedUser(e);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center -mt-40 w-full h-full bg-gray-100">
        <CircularProgress />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center -mt-40 w-full h-full gap-2 bg-gray-100">
        <h6 className="text-gray-900">No data found.</h6>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gray-100 px-20 pt-20">
      <div className="flex flex-row justify-between items-center text-gray-900">
        <h2 className="text-2xl">{data?.title ? data.title : "Form Title"}</h2>
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
            value={selectedUser}
            label="Selected User"
            onChange={(e) => handleUserSelection(e.target.value)}
          >
            {userList &&
              userList.length > 0 &&
              userList.map((u, idx) => {
                const user_name = u.name;
                return <MenuItem value={user_name}>{user_name}</MenuItem>;
              })}
            {/* <MenuItem value="Panya">Panya</MenuItem>
            <MenuItem value="Daveraj">Daveraj</MenuItem>
            <MenuItem value="Saranya">Saranya</MenuItem>
            <MenuItem value="Maks">Maks</MenuItem> */}
          </Select>
        </FormControl>
      </div>
      <div className="flex mt-10 w-full h-screen text-gray-900">
        {data &&
          data.map((d, index) => {
            return (
              <div key={index}>
                <h2 className="text-gray-500 font-bold text-2xl">
                  {d.question}
                </h2>
                <h3 className="text-gray-500 font-light text-xl">{d.answer}</h3>
              </div>
            );
          })}
      </div>
    </div>
  );
};

export default ViewData;
