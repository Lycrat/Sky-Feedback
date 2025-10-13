import { useParams } from "react-router";
import QuestionCreator from "../components/QuestionCreator";
import { useState } from "react";

function AddEditPage({mode = "create" }) {
    let initialData = null
    if (mode == "edit") {
        const questionnaire_id = useParams().id
        console.log(questionnaire_id)
        initialData = {
            title: "test",
            questions : 
                [
                    {id : 1, text: "test question", type: "textarea", options: []}
                ] 
            
        }
    }

    const [formTitle, setFormTitle] = useState(initialData?.title || "");
    const [questions, setQuestions] = useState(initialData?.questions || []);

    const handleQuestionsChange = (updatedQuestions) => {
        setQuestions(updatedQuestions);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        const formData = {
        title: formTitle,
        questions: questions,
        };
        
        console.log(`${mode === "edit" ? "Updating" : "Creating"} Form Data:`, formData);        
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
                initialQuestions={initialData?.questions}
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

export default AddEditPage;