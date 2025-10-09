import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { Layout } from "./components";
import { UserQuestionaire } from "./pages";
function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<h1>PUT HOME DASHBOARD HERE</h1>} />
            <Route path="/questionaire/:id" element={<UserQuestionaire />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
