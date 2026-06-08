import { getCustomFoods, getRecipes } from "../../api/utils";
import { useEffect, useState } from "react";
import { components } from "../../types/api";
import CustomFood from "./CustomFood";

export type FoodOut = components["schemas"]["FoodOut"];

function Recipes({ recipes }) {
  return (
    <div>
      <h1>[PLACEHOLDER] Recipes</h1>
    </div>
  );
}

export default function CustomBase() {
  const [activeTab, setActivateTab] = useState("custom-foods");
  const [customFood, setCustomFood] = useState([]);
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    const fetchCustomFood = async () => {
      const food = await getCustomFoods();
      setCustomFood(food);
    };
    fetchCustomFood();
  }, []);

  useEffect(() => {
    const fetchRecipes = async () => {
      const recipeList = await getRecipes();
      setRecipes(recipeList);
    };
    fetchRecipes();
  }, []);

  const base = "rounded-full px-4 py-2 text-sm font-medium transition-colors";
  const inactive = "bg-gray-200 text-gray-700 hover:bg-gray-300";
  const active = "bg-blue-600 text-white hover:bg-blue-700";

  return (
    <div>
      <div role="tablist" className="flex gap-2">
        <button
          onClick={(e) => setActivateTab(e.currentTarget.value)}
          value="custom-foods"
          role="tab"
          aria-selected="true"
          className={`${base} ${activeTab === "custom-foods" ? active : inactive}`}
        >
          Custom Foods
        </button>

        <button
          onClick={(e) => setActivateTab(e.currentTarget.value)}
          value="recipes"
          role="tab"
          aria-selected="true"
          className={`${base} ${activeTab === "recipes" ? active : inactive}`}
        >
          Recipes
        </button>

        <button
          onClick={(e) => setActivateTab(e.currentTarget.value)}
          value="placeholder"
          role="tab"
          aria-selected="true"
          className={`${base} ${activeTab === "placeholder" ? active : inactive}`}
        >
          Placeholder
        </button>
      </div>

      <div role="tabpanel" className="mt-4">
        {activeTab === "custom-foods" && <CustomFood customFood={customFood} />}
        {activeTab === "recipes" && <Recipes recipes={recipes} />}
        {activeTab === "placeholder" && (
          <div>
            <h1>[PLACEHOLDER] </h1>
          </div>
        )}
      </div>
    </div>
  );
}

/* 
list all customfoods in list element with dropdown for hiding
list all recipes in list element
have add custom food button, have add recipe button. 
    place button in respective dropdown
form to appear on right side
customFood form
addRecipeForm

*/
