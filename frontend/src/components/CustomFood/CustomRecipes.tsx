import { useState, useEffect } from "react";
import FoodEntryItemSelector from "../SearchFood/FoodEntryItemSelector";
import { FoodEntryFormContextProvider } from "../Tracker/FoodEntryFormContext";
import FoodEntryForm from "../SearchFood/FoodEntryForm";
import FoodResultList from "../SearchFood/FoodResultsList";
import FoodSearchBar from "../SearchFood/FoodSearchBar";
import { searchFoodByName, getRecipes } from "../../api/utils";
import RecipesList from "./RecipesList";

export default function CustomRecipes() {
  const [searchText, setSearchText] = useState("");
  const [foodSearchResults, setFoodSearchResults] = useState(null);
  const [recipes, setRecipes] = useState([]);
  const [reloadTracker, setReloadTracker] = useState(0);

  const reload = () => {
    const count = reloadTracker + 1;
    setReloadTracker(count);
  };

  useEffect(() => {
    const fetchCustomRecipes = async () => {
      const recipes = await getRecipes();
      setRecipes(recipes);
    };
    fetchCustomRecipes();
  }, [reloadTracker]);

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
    <div className="flex">
      <FoodEntryFormContextProvider reload={reload}>
        <RecipesList recipes={recipes} />
        <FoodEntryItemSelector />
        <div>
          <FoodEntryForm />
          <FoodSearchBar setSearchText={setSearchText} />
          <FoodResultList foodSearchResults={foodSearchResults} />
        </div>
      </FoodEntryFormContextProvider>
    </div>
  );
}
