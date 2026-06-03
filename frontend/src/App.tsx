import "./App.css";
import "./components/DateSelector.js";
import BaseLayout from "./layouts/BaseLayout.tsx";
import { BrowserRouter, Route, Routes } from "react-router";
import { ROUTES } from "./routes.ts";
import Login from "./components/Login.tsx";
import Tracker from "./components/Tracker.tsx";

function App() {
  return (
    <BaseLayout>
      <BrowserRouter>
        <Routes>
          <Route path={ROUTES.TRACKER} element={<Tracker />} />
          <Route
            path={ROUTES.CUSTOM_FOODS}
            element={<div>PLACEHOLDER CUSTOM FOODS</div>}
          />
          <Route
            path={ROUTES.STATISTICS}
            element={<div>PLACEHOLDER STATS</div>}
          />
          <Route path={ROUTES.LOGIN} element={<Login />} />
        </Routes>
      </BrowserRouter>
    </BaseLayout>
  );
}

export default App;
