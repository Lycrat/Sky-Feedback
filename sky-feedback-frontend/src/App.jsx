import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { Layout } from "./components";
import { UserQuestionaire, AddEditWrapper } from "./pages";
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
            <Route path="/view-data/:formId" element={<ViewData />} />
            <Route path="/create-form" element={<AddEditWrapper />}/>
            <Route path="/edit/:id" element={<AddEditWrapper mode="edit" />}/>
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
