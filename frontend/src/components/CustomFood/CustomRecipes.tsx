import { useState, useEffect, useContext } from "react";
import FoodEntryItemSelector from "../SearchFood/FoodEntryItemSelector";
import {
  FoodEntryFormContextProvider,
  FoodEntryFormContext,
} from "../Tracker/FoodEntryFormContext";
import FoodEntryForm from "../SearchFood/FoodEntryForm";
import FoodResultList from "../SearchFood/FoodResultsList";
import FoodSearchBar from "../SearchFood/FoodSearchBar";
import {
  searchFoodByName,
  addRecipeToLog,
  deleteRecipe,
  getRecipes,
} from "../../api/utils";

function RecipesList({ recipes }) {
  const context = useContext(FoodEntryFormContext);
  const setSelectorData = context.setSelectorData;
  const setFormTarget = context.setFormTarget;
  const setFormMode = context.setFormMode;

  const recipeList = recipes?.map((recipe) => (
    <tr key={recipe.id} className="border">
      <td>
        <button
          onClick={() => {
            addRecipeToLog(recipe.id);
          }}
        >
          Add
        </button>
      </td>

      <td>
        <p className="text-sm font-medium text-heading truncate">
          <strong>{recipe.recipe_name}</strong>
        </p>
      </td>
      <td>{recipe.kcal.toFixed(1)} kcal</td>
      <td>
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
      </td>
      <td>
        <button
          onClick={() => {
            deleteRecipe(recipe.id);
          }}
        >
          X
        </button>
      </td>
    </tr>
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
        <table className="border">
          <thead className="border">
            <tr>
              <td></td>
              <td>
                <strong>Recipe Name</strong>
              </td>
              <td>
                <strong>Calories</strong>
              </td>
              <td></td>
              <td></td>
            </tr>
          </thead>
          {recipeList}
        </table>
        <ul className="divide-y divide-default a border"></ul>
      </div>
    </div>
  );
}

export default function CustomRecipes() {
  const [searchText, setSearchText] = useState("");
  const [foodSearchResults, setFoodSearchResults] = useState(null);
  const [recipes, setRecipes] = useState(null);
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
      <FoodEntryFormContextProvider>
        <RecipesList recipes={recipes} />
        <FoodEntryItemSelector reload={reload} />
        <div>
          <FoodEntryForm />
          <FoodSearchBar setSearchText={setSearchText} />
          <FoodResultList foodSearchResults={foodSearchResults} />
        </div>
      </FoodEntryFormContextProvider>
    </div>
  );
}
