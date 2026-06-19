import { FoodEntryFormContextProvider } from "./FoodEntryFormContext.tsx";
import { format } from "date-fns";
import { useState, useEffect, useContext } from "react";
import DailyLog from "./DailyLog.tsx";
import DateSelector from "./DateSelector.tsx";
import FoodSummary from "./FoodSummary.tsx";
import FoodSearchBar from "../SearchFood/FoodSearchBar.tsx";
import FoodResultList from "../SearchFood/FoodResultsList.tsx";
import FoodEntryForm from "../SearchFood/FoodEntryForm.tsx";
import { getFoodEntriesForDate, searchFoodByName } from "../../api/utils.ts";
import FoodEntryItemSelector from "../SearchFood/FoodEntryItemSelector.tsx";
import { FoodEntryFormContext } from "../Tracker/FoodEntryFormContext.tsx";

function AddFoodButton() {
  const context = useContext(FoodEntryFormContext);
  if (!context) {
    throw new Error(
      "Component must be used inside FoodEntryFormContextProvider",
    );
  }
  const openNewEntryToLog = context.openNewEntryToLog;

  return (
    <button onClick={() => openNewEntryToLog()}>Create New Food Entry</button>
  );
}

export default function Tracker() {
  function getDate() {
    const timestamp = Date.now();
    const date = new Date(timestamp);
    return date;
  }

  const fetchFoodData = async () => {
    const formattedDate = format(date, "yyyy-MM-dd");
    const foodEntries = await getFoodEntriesForDate(formattedDate);
    setFoodData(foodEntries);
  };

  const [foodData, setFoodData] = useState([]);
  const [date, setDate] = useState(getDate());
  const [reloadTracker, setReloadTracker] = useState(0);
  useEffect(() => {
    fetchFoodData();
    console.log(reloadTracker);
  }, [date, reloadTracker]);

  const reload = () => {
    const count = reloadTracker + 1;
    setReloadTracker(count);
  };

  const [searchText, setSearchText] = useState("");
  const [foodSearchResults, setFoodSearchResults] = useState(null);

  useEffect(() => {
    if (!searchText) {
      setFoodSearchResults(null);
      return;
    }
    const t = setTimeout(() => {
      const fetchResults = async () => {
        const searchResults = await searchFoodByName(searchText);
        setFoodSearchResults(searchResults);
      };
      fetchResults();
    }, 500);
    return () => clearTimeout(t);
  }, [searchText]);

  return (
    <div>
      <FoodEntryFormContextProvider reload={reload}>
        <div className="flex justify-evenly items-center">
          <DateSelector date={date} setDate={setDate} />
          <FoodSummary foodData={foodData} />
          <AddFoodButton />
        </div>
        <DailyLog foodData={foodData} fetchFoodData={fetchFoodData} />
        <div className="flex justify-evenly">
          <div>
            <FoodEntryItemSelector reload={reload} />
            <FoodEntryForm />
          </div>
          <div>
            <FoodSearchBar setSearchText={setSearchText} />
            <FoodResultList foodSearchResults={foodSearchResults} />
          </div>
        </div>
      </FoodEntryFormContextProvider>
    </div>
  );
}
