import { Link, useNavigate } from "react-router"
/**
 * 
 * @param {object} data 
 * Each object should have at least:
 *  - questionnaire_id (number)
 *  - cardTitle (string)
 */
function FormCard ({data}) {
    let navigate = useNavigate()
    return (
        <div className="flex-col bg-slate-200 p-5 rounded-[2vw] min-w-[350px] max-w-[350px] h-[150px]">
            <Link to={`/questionnaire/${data.id}`}
                className=""
            >
                <h2 className="text-black my-4 justify-self-center min-w-[300px] hover:">{data.title}</h2>
            </Link>
            <span className="justify-self-center space-x-2">
                <button className="bg-blue-500 w-[150px] hover:bg-blue-600 text-white font-semibold rounded-lg transition duration-200 my-2" onClick={(e) => navigate(`/edit/${data.id}`)}>Edit</button>
                <button className="bg-green-500 w-[150px] hover:bg-green-600 text-white font-semibold rounded-lg transition duration-200 my-2" onClick={(e) => navigate(`/answers/${data.id}`)}>View Answers</button>
            </span>
        </div>
    )
};

export default FormCard;