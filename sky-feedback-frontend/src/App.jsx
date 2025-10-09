import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { Layout } from "./components";
import { UserQuestionaire } from "./pages";
import QuestionCreator from "./components/QuestionCreator";
import HomeDashboard from "./pages/HomeDashboard";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomeDashboard />} />
            <Route path="/questionnaire/:id" element={<UserQuestionaire />} />
            <Route path="question-creator" element={<QuestionCreator />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
