import { useState } from "react";
import CustomFood from "./CustomFood";
import CustomRecipes from "./CustomRecipes";

export default function CustomBase() {
  const [activeTab, setActivateTab] = useState("custom-foods");

  const base = "rounded-full px-4 py-2 text-sm font-medium transition-colors";
  const inactive = "bg-gray-200 text-gray-700 hover:bg-gray-300";
  const active = "bg-blue-600 text-white hover:bg-blue-700";

  /* TODO: on tab change, reset data*/
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
        {activeTab === "custom-foods" && <CustomFood />}
        {activeTab === "recipes" && <CustomRecipes />}
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
