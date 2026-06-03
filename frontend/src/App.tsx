import axios from "axios";
import { useState, useEffect } from "react";
import "./App.css";
import "./components/DateSelector.js";
import DateSelector from "./components/DateSelector.js";
import FoodItemList from "./components/FoodItemList.js";
import FoodSummary from "./components/FoodSummary.js";
import FoodSearchBar from "./components/SearchFood/FoodSearchBar.js";
import FoodResultList from "./components/SearchFood/FoodResultsList.js";
import { api } from "./api/client";
import { format } from "date-fns";
import FoodEntryForm from "./components/SearchFood/FoodEntryForm.tsx";
import type { components } from "./types/api.ts";
import BaseLayout from "./layouts/BaseLayout.tsx";
import { BrowserRouter, Route, Routes } from "react-router";
import { ROUTES } from "./routes.ts";
import Login from "./components/Login.tsx";

type FoodOut = components["schemas"]["FoodOut"];

function BaseApp() {
  function getDate() {
    const timestamp = Date.now();
    const date = new Date(timestamp);
    return date;
  }

  const fetchFoodData = async () => {
    const response = await api.get(
      `/api/food_get/search/date/${format(date, "yyyy-MM-dd")}`,
    );
    setFoodData(response.data);
  };

  const [date, setDate] = useState(getDate());
  const [foodData, setFoodData] = useState([]);
  useEffect(() => {
    fetchFoodData();
  }, [date]);

  const [searchText, setSearchText] = useState("");
  const [foodSearchResults, setFoodSearchResults] = useState(null);
  const [showFoodResultsSection, setShowFoodResultsSection] = useState(false);

  useEffect(() => {
    if (!searchText) {
      setFoodSearchResults(null);
      return;
    }
    const t = setTimeout(() => {
      const fetchResults = async () => {
        const response = await api.get(
          `/api/food_get/search/name/${searchText}`,
        );
        setFoodSearchResults(response.data);
        return response.data;
      };
      fetchResults();
    }, 500);
    return () => clearTimeout(t);
  }, [searchText]);

  /* Add/Edit Food Form Values */
  const [foodEntryFormData, setFoodEntryFormData] = useState<FoodOut | null>(
    null,
  );
  const [foodEntryFormVisible, setFoodEntryFormVisible] = useState(false);
  const [existingGrams, setExistingGrams] = useState(100);
  const [foodEntryItemID, setFoodEntryItemID] = useState("placeholder");
  const [formMode, setFormMode] = useState<"add" | "edit">("add");

  return (
    <div className="main space-x-10 space-y-15">
      <div className="flex justify-evenly items-center">
        <DateSelector date={date} setDate={setDate} />

        <FoodSummary foodData={foodData} />
      </div>

      <div>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
          onClick={() => setShowFoodResultsSection(!showFoodResultsSection)}
        >
          Add Food
        </button>
      </div>

      <FoodItemList
        foodData={foodData}
        fetchFoodData={fetchFoodData}
        setFoodEntryFormData={setFoodEntryFormData}
        setFoodEntryFormVisible={setFoodEntryFormVisible}
        setFormMode={setFormMode}
        setFoodEntryItemID={setFoodEntryItemID}
        setExistingGrams={setExistingGrams}
      />

      <div className="flex justify-evenly items-center">
        {showFoodResultsSection && (
          <section>
            <FoodSearchBar setSearchText={setSearchText} />

            <FoodResultList
              foodSearchResults={foodSearchResults}
              date={date}
              setFoodEntryFormData={setFoodEntryFormData}
              setFormMode={setFormMode}
              setFoodEntryFormVisible={setFoodEntryFormVisible}
            />
          </section>
        )}

        <FoodEntryForm
          FoodOutData={foodEntryFormData}
          FoodEntryItemId={foodEntryItemID}
          isVisible={foodEntryFormVisible}
          setVisible={setFoodEntryFormVisible}
          mode={formMode}
          existingGrams={existingGrams}
        />
      </div>
    </div>
  );
}

function App() {
  return (
    <BaseLayout>
      <BrowserRouter>
        <Routes>
          <Route path={ROUTES.TRACKER} element={<BaseApp />} />
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
