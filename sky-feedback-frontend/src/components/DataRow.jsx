import React from "react";

export const DataRow = ({ answerObj, question }) => {
  return (
    <div>
      <h2 className="text-gray-500 font-bold text-2xl">{question}</h2>
      {console.log(answerObj, question)}
      {answerObj && answerObj.feedback.length > 0 ? (
        answerObj.feedback.map((fb, idx) => (
          <h3 key={idx} className="text-gray-500 font-light text-xl">
            - {fb.feedback}
          </h3>
        ))
      ) : (
        <h3 className="text-red-300 font-light text-xl">No feedback yet</h3>
      )}
    </div>
  );
};

export default DataRow;
