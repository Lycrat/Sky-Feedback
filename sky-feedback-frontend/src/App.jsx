import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { Layout } from "./components";
import { UserQuestionaire, AddEditPage } from "./pages";
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
            <Route path="/create-form" element={<AddEditPage />}/>
            <Route path="/edit/:id" element={<AddEditPage mode="edit" />}/>
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
