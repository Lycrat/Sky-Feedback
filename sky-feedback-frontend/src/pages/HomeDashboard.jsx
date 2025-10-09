import FormCardContainer from "../components/FormCardContainer";

const questionnaires = [
  {
    "questionnaire_id": 1,
    "cardTitle": "Customer Feedback Survey"
  }
]

function HomeDashboard () {
    return(
        <>  
            <h1 className="text-5xl m-[1vw] justify-self-center">My Forms</h1>
            <FormCardContainer data={questionnaires}/>
        </>
    )
}



export default HomeDashboard;