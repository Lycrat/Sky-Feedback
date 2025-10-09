import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { Layout } from "./components";
import { UserQuestionaire } from "./pages";
import QuestionCreator from "./components/QuestionCreator";
import HomeDashboard from "./pages/HomeDashboard";

import ViewData from "./pages/ViewData";
function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomeDashboard />} />
            <Route path="/questionnaire/:id" element={<UserQuestionaire />} />
            <Route path="/view-data" element={<ViewData />} />
          </Route>
          <Route path="question-creator" element={<QuestionCreator />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
