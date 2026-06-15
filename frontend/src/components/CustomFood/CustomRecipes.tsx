import { useState, useEffect, useContext } from "react";
import FoodEntryItemSelector from "../SearchFood/FoodEntryItemSelector";
import {
  FoodEntryFormContextProvider,
  FoodEntryFormContext,
} from "../Tracker/FoodEntryFormContext";
import FoodEntryForm from "../SearchFood/FoodEntryForm";
import FoodResultList from "../SearchFood/FoodResultsList";
import FoodSearchBar from "../SearchFood/FoodSearchBar";
import { searchFoodByName } from "../../api/utils";

function RecipesList({ recipes }) {
  const context = useContext(FoodEntryFormContext);
  const setSelectorData = context.setSelectorData;
  const setFormTarget = context.setFormTarget;
  const setFormMode = context.setFormMode;

  const recipeList = recipes.map((recipe) => (
    <li key={recipe.id} className="pb-3 sm:pb-4">
      <div className="flex items-center space-x-4- rlt:space-x-reverse">
        <p className="text-sm font-medium text-heading truncate">
          <strong>
            {recipe.recipe_name} | {recipe.kcal} kcal |
          </strong>
          <button
            onClick={() => {
              /* TODO: create helper function */
              setSelectorData(recipe);
              setFormTarget("recipe");
              setFormMode("edit"); /* why add? */
            }}
          >
            Edit
          </button>
        </p>
      </div>
    </li>
  ));
  return (
    <div>
      <div>
        <button
          onClick={() => {
            /* TODO: create helper function */
            setSelectorData({ food_items: [], recipe_name: "" });
            setFormTarget("recipe");
            setFormMode("add");
          }}
        >
          Create New Custom Recipe
        </button>
        <ul className="divide-y divide-default a border">{recipeList}</ul>
      </div>
    </div>
  );
}

export default function CustomRecipes({ recipes }) {
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
    <div className="flex">
      <FoodEntryFormContextProvider>
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
