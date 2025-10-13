import { useNavigate, useParams } from "react-router";
import QuestionCreator from "../components/QuestionCreator";
import { useState, useEffect } from "react";
import axios from "axios";

const API_KEY = import.meta.env.VITE_API_URL

function AddEditPage({mode = "create"}) {
    let navigate = useNavigate();
    const formId = useParams().id;
    const [formTitle, setFormTitle] = useState("");
    const [questions, setQuestions] = useState([]);
    

    useEffect(() => {
        if (mode === "edit") {
            fetchFormData();
        }
    }, [mode, formId]);

    const fetchFormData = async () => {        
            try {
                const response = await axios.get(API_KEY + '/api/questionnaire/' + formId);
                const data = response.data;
                setFormTitle(data.questionnaire[0]?.title || "");
                setQuestions(data.questions || []);
            } catch (error) {
                console.error(error);
            }
    };

    const handleQuestionsChange = (updatedQuestions) => {
        setQuestions(updatedQuestions);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const questionData = questions.map(question => question.text)

        const formData = {
        title: formTitle,
        questions_list: questionData,
        };
        console.log(formData)
        
        console.log(`${mode === "edit" ? "Updating" : "Creating"} Form Data:`, formData);
        
        try {
            if (mode === "edit") {
                const response = await axios.put(API_KEY + '/api/questionnaire/' + formId, formData);
                console.log(response.data)
            } else {
                const response = await axios.post(API_KEY + '/api/questionnaire/', formData);
                console.log(response.data);
            } 
        } catch (err) {
            console.error("Error submitting form:", err);
            alert("Error submitting form. Check console.");
        }
        navigate('/');
    };

    return (
        <div className="max-w-4xl mx-auto min-h-screen">
            <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            {mode === "edit" ? "Edit Your Form" : "Create Your Form"}
            </h1>

            <div className="space-y-6">
                <div className="bg-white rounded-2xl p-8 shadow-md border border-gray-200">
                    <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Form Title *
                    </label>
                    <input
                        type="text"
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value={formTitle}
                        onChange={(e) => setFormTitle(e.target.value)}
                        placeholder="Enter form title"
                        required
                    />
                    </div>
                
                </div>

                <div className="flex justify-center">
                <QuestionCreator 
                    onQuestionChange={handleQuestionsChange}
                    initialQuestions={questions}
                />
                </div>

                <div className="flex justify-center">
                    <button
                    onClick={handleSubmit}
                    className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium text-lg shadow-md"
                    >
                    {mode === "edit" ? "Update Form" : "Submit Form"}
                    </button>
                </div>
            </div>
        </div>
    );
    }

function AddEditWrapper({ mode }) {
  const { id } = useParams();
  return <AddEditPage key={id} mode={mode} />;
}


export default AddEditWrapper;