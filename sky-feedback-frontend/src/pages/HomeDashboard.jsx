import { useState, useEffect } from "react";
import FormCardContainer from "../components/FormCardContainer";
import axios from "axios";

function HomeDashboard () {
  const [questionnaires, setQuestionnaires] = useState([])
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/questionnaire/");
        setQuestionnaires(response.data);
      } catch (err) {
        console.error("Error fetching data:", err);
      } 
    };
    fetchData();
  }, []); 


    return(
        <>  
            <h1 className="text-5xl font-light justify-self-center">My Forms</h1>
            <FormCardContainer data={questionnaires}/>
        </>
    )
}



export default HomeDashboard;