import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { CircularProgress, Typography } from '@mui/material';

const apiUrl = import.meta.env.VITE_API_URL;

export const ViewData = ({ id }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const handleFetchData = async () => {
      try {
        const response = await axios.get(`${apiUrl}/${id}`);
        if (response.status === 200) {
          setData(response.data);
          console.log("Successful")
        } else {
          console.error('Request was unsuccessful');
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    handleFetchData();
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <CircularProgress />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-2">
        <Typography variant="h6" color="textSecondary">
          No data found.
        </Typography>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-4 bg-gray-100 p-6 rounded-xl shadow-md">
      <Typography variant="h4" style={{ fontWeight: 600 }}>
        {data.title || 'No Title'}
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        {data.user || 'Unknown User'}
      </Typography>
    </div>
  );
};

export default ViewData;
