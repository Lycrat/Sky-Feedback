import React from "react"
import FormCard from "./FormCard"
import { useNavigate } from "react-router"

/**
 * Renders a list of FormCard components based on the provided data array.
 *
 * @param {Object[]} data - The array of questionnaire data objects.
 * Each object should have at least:
 *  - questionnaire_id (number)
 *  - cardTitle (string)
 */
function FormCardContainer ({data}) {
    let navigate = useNavigate()
    if (!Array.isArray(data) || data.length === 0) {
        return (
            <div className="grid [grid-template-columns:repeat(auto-fit,minmax(350px,1fr))] gap-8 p-6 w-full place-items-center">
                <button
                    type="button"
                    onClick={() => navigate("/create-form")}
                    className="flex items-center justify-center bg-slate-200 hover:bg-slate-300 p-5 rounded-[2vw] m-[10px] w-[350px] h-[150px] text-6xl text-gray-500 font-bold transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
                >
                    +
                </button>
            </div>
            )
    } else {
        return (
            <div className="grid [grid-template-columns:repeat(auto-fit,minmax(350px,1fr))] gap-8 p-6 w-full place-items-center">
                {data.map((item) => (
                    <FormCard key={item.questionnaire_id} data={item} />
                ))}
            <button
                type="button"
                onClick={() => navigate("/create-form")}
                className="flex items-center justify-center bg-slate-200 hover:bg-slate-300 p-5 rounded-[2vw] m-[10px] w-[350px] h-[150px] text-6xl text-gray-500 font-bold transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
                +
            </button>
        </div>
        )
    }
}

export default FormCardContainer;