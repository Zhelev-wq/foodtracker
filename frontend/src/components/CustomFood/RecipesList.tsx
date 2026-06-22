import { useContext } from "react";
import { FoodEntryFormContext } from "../Tracker/FoodEntryFormContext";
import { components } from "../../types/api";
import { addRecipeToLog, deleteRecipe } from "../../api/utils";

type RecipeOutput = components["schemas"]["RecipeOutput"];
type RecipeListProps = {
  recipes: RecipeOutput[];
};

export default function RecipesList({ recipes }: RecipeListProps) {
  const context = useContext(FoodEntryFormContext);
  if (!context) {
    throw new Error(
      "Component must be used inside FoodEntryFormContextProvider",
    );
  }
  const openNewEmptyRecipe = context.openNewEmptyRecipe;
  const openEditRecipe = context.openEditRecipe;

  const recipeList = recipes?.map((recipe: RecipeOutput) => (
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
          <strong>{recipe.name}</strong>
        </p>
      </td>
      <td>{recipe.kcal.toFixed(1)} kcal</td>
      <td>
        <button onClick={() => openEditRecipe(recipe)}>Edit</button>
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
        <button onClick={() => openNewEmptyRecipe()}>
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
