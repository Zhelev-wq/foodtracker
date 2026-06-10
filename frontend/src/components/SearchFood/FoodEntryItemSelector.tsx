import React, { useContext } from "react";
import { CustomRecipeFormContext } from "../CustomFood/CustomRecipeFormContext";
import { saveFoodEntryEdit } from "../../api/utils";

type FoodEntryItemSelectorProps = {
  formContext: React.Context;
};

export default function FoodEntryItemSelector({
  formContext,
}: FoodEntryItemSelectorProps) {
  const context = useContext(formContext);
  const foodEntryItems = context.selectorData;
  const setSelectorData = context.setSelectorData;
  const openEdit = context.openEdit;
  const setFormTarget = context.setFormTarget;
  const foodEntryID = context.foodEntryID;

  if (!foodEntryItems || foodEntryItems.length === 0) {
    return null;
  }

  function AddFoodButton() {
    return (
      <button
        onClick={() => {
          setFormTarget("food-entry");
        }}
      >
        Add Food
      </button>
    );
  }

  function SaveRecipeButton() {
    return (
      <button
        onClick={() => {
          saveFoodEntryEdit(foodEntryItems, foodEntryID);
          window.location.reload();
        }}
      >
        Save Recipe
      </button>
    );
  }

  const formattedResults = foodEntryItems.map((foodEntryItem) => (
    <li key={foodEntryItem.id} className="pb-3 sm:pb-4">
      <div className="flex justify-evenly space-x-4- rlt:space-x-reverse">
        <p className="text-sm font-medium text-heading truncate">
          <strong>
            {foodEntryItem.food.name} |
            {(foodEntryItem.food.kcal * foodEntryItem.food_grams) / 100} kcal |
            {foodEntryItem.food_grams} g
          </strong>
        </p>
        <button
          onClick={() => {
            setFormTarget("food-entry");
            openEdit(foodEntryItem); /* -> opens FoodEntryForm */
          }}
        >
          Edit
        </button>
      </div>
    </li>
  ));

  return (
    <div>
      <div className="flex justify-evenly">
        <h2>Select Food Item</h2>
        <button
          onClick={() => {
            setSelectorData([]);
          }}
        >
          X
        </button>
      </div>
      <ul className="max-w-md divide-y divide-default a border">
        {formattedResults}
      </ul>
      <div className="flex justify-evenly">
        <AddFoodButton />
        <SaveRecipeButton />
      </div>
    </div>
  );
}
