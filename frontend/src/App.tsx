import "./App.css";
import "./components/DateSelector.js";
import BaseLayout from "./layouts/BaseLayout.tsx";
import { BrowserRouter, Route, Routes } from "react-router";
import { ROUTES } from "./routes.ts";
import Login from "./components/Login.tsx";
import Tracker from "./components/Tracker.tsx";
import Register from "./components/Register.tsx";
import CustomBase from "./components/CustomFood/CustomBase.tsx";

function App() {
  return (
    <BaseLayout>
      <BrowserRouter>
        <Routes>
          <Route path={ROUTES.TRACKER} element={<Tracker />} />
          <Route path={ROUTES.CUSTOM_FOODS} element={<CustomBase />} />
          <Route
            path={ROUTES.STATISTICS}
            element={<div>PLACEHOLDER STATS</div>}
          />
          <Route path={ROUTES.LOGIN} element={<Login />} />
          <Route path={ROUTES.REGISTER} element={<Register />} />
        </Routes>
      </BrowserRouter>
    </BaseLayout>
  );
}

export default App;
