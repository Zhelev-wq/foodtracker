import { useContext } from "react";
import { FoodEntryFormContext } from "../Tracker/FoodEntryFormContext";
import { DraftItem } from "../../types/draft";

// saved items store grams as food_grams; new (unsaved) items store it as grams
function itemGrams(item: DraftItem): number {
  return "food_grams" in item ? item.food_grams : item.grams;
}

export default function FoodEntryItemSelector() {
  const context = useContext(FoodEntryFormContext);
  if (!context) {
    throw new Error(
      "Component must be used inside FoodEntryFormContextProvider",
    );
  }
  const selectorData = context.selectorData;
  const openEdit = context.openEdit;
  const removeItemFromEntry = context.removeItemFromEntry;
  const setRecipeName =
    context.setRecipeName; /*TODO: what does this do. do I need it? */
  const setShowSearchBar = context.setShowSearchBar;
  const foodIdOf = context.foodIdOf;
  const saveRecipe = context.saveRecipe;
  const closeSelector = context.closeSelector;

  if (!selectorData) {
    /* if selectorData is empty or foodEntryID not new */
    return null;
  }

  function AddFoodButton() {
    return (
      <button
        onClick={() => {
          setShowSearchBar(true);
        }}
      >
        Add Food
      </button>
    );
  }

  function SaveRecipeButton() {
    return (
      <button onClick={async () => await saveRecipe()}>Save Recipe</button>
    );
  }

  function FormattedResults() {
    if (selectorData) {
      const formattedResults = selectorData?.food_items?.map(
        (foodEntryItem: DraftItem) => (
          <li key={foodIdOf(foodEntryItem)} className="pb-3 sm:pb-4">
            <div className="flex gap-4 justify-between items-center">
              <button
                onClick={() => {
                  // new items aren't saved yet, so they can't be edited this way
                  if ("food_id" in foodEntryItem) {
                    openEdit(foodEntryItem); /* -> opens FoodEntryForm */
                  }
                }}
              >
                Edit
              </button>
              <p className="text-sm font-medium text-heading truncate">
                <strong>
                  {foodEntryItem.food.name} |
                  {(
                    (foodEntryItem.food.kcal * itemGrams(foodEntryItem)) /
                    100
                  ).toFixed(1)}{" "}
                  kcal |{itemGrams(foodEntryItem)} g
                </strong>
              </p>
              <button
                className="ml-auto"
                onClick={() => {
                  removeItemFromEntry(foodEntryItem);
                }}
              >
                Remove
              </button>
            </div>
          </li>
        ),
      );
      return formattedResults;
    }
    return null;
  }

  return (
    <div>
      <div className="flex justify-evenly">
        <h2>Select Food Item</h2>
        <button
          onClick={() => {
            closeSelector();
          }}
        >
          X
        </button>
      </div>

      <input /* TODO: disappear during dailyLog editing */
        name="recipe-name"
        value={selectorData?.recipe_name ?? ""}
        onChange={(e) => setRecipeName(e.target.value)}
      />

      <ul className="max-w-md divide-y divide-default a border">
        <FormattedResults />
      </ul>
      <div className="flex justify-evenly">
        <AddFoodButton />
        <SaveRecipeButton />
      </div>
    </div>
  );
}
