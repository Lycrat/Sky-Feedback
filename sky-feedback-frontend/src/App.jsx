import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { Layout } from "./components";
import QuestionCreator from "./components/QuestionCreator";
import ViewData from "./pages/ViewData";
function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<h1>PUT HOME DASHBOARD HERE</h1>} />
            <Route path="/view-data" element={<ViewData />} />
          </Route>
          <Route path="question-creator" element={<QuestionCreator />}></Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
