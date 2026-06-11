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

function AddFoodButton({ contextProp }) {
  const context = useContext(contextProp);
  const setFormTarget = context.setFormTarget;
  const setSelectorData = context.setSelectorData;

  return (
    <button
      onClick={() => {
        setFormTarget("daily-log");
        setSelectorData(null);
      }}
    >
      ADD FOOD
    </button>
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

  const [date, setDate] = useState(getDate());
  const [foodData, setFoodData] = useState([]);
  useEffect(() => {
    fetchFoodData();
  }, [date]);

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
      <FoodEntryFormContextProvider>
        <div className="flex justify-evenly items-center">
          <DateSelector date={date} setDate={setDate} />
          <FoodSummary foodData={foodData} />
          <AddFoodButton contextProp={FoodEntryFormContext} />
        </div>
        <DailyLog foodData={foodData} fetchFoodData={fetchFoodData} />
        <div className="flex justify-evenly">
          <div>
            <FoodEntryItemSelector formContext={FoodEntryFormContext} />
            <FoodEntryForm contextProp={FoodEntryFormContext} />
          </div>
          <div>
            <FoodSearchBar
              setSearchText={setSearchText}
              contextProp={FoodEntryFormContext}
            />
            <FoodResultList
              foodSearchResults={foodSearchResults}
              context={FoodEntryFormContext}
            />
          </div>
        </div>
      </FoodEntryFormContextProvider>
    </div>
  );
}
