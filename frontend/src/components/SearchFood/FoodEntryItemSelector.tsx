import React, { useContext, useState } from "react";
import { saveFoodEntryEdit } from "../../api/utils";
import { FoodEntryFormContext } from "../Tracker/FoodEntryFormContext";

export default function FoodEntryItemSelector() {
  const context = useContext(FoodEntryFormContext);
  const selectorData = context.selectorData;
  const setSelectorData = context.setSelectorData;
  const openEdit = context.openEdit;
  const setFormTarget = context.setFormTarget;
  const removeItemFromEntry = context.removeItemFromEntry;
  const formTarget = context.formTarget;
  const commitFoodComposition = context.commitFoodComposition;
  const setRecipeName = context.setRecipeName;
  const setFormMode = context.setFormMode;
  const setShowSearchBar = context.setShowSearchBar;
  const foodIdOf = context.foodIdOf

  if (!selectorData) {
    /* if selectorData is empty or foodEntryID not new */
    return null;
  }

  function AddFoodButton() {
    return (
      <button
        onClick={() => {
          /* TODO: figure out how to make this work*/
          setShowSearchBar(true);
        }}
      >
        Add Food
      </button>
    );
  }

  function SaveRecipeButton() {
    return (
      <button
        onClick={async () => {
          if (formTarget === "recipe") {
            await commitFoodComposition(); /* only create implemented. TODO: add visual element to confirm  */
          } else if (formTarget === "food-entry") {
            saveFoodEntryEdit(
              selectorData,
            ); /* method part of commitFoodComposition() replace entire ifelse with it after testing*/
          }
          /*
          window.location.reload();
          */
        }}
      >
        Save Recipe
      </button>
    );
  }

  function FormattedResults() {
    if (selectorData) {
      const formattedResults = selectorData.food_items.map((foodEntryItem) => (
        <li key={foodIdOf(foodEntryItem)} className="pb-3 sm:pb-4">
          <div className="flex gap-4 justify-between items-center">
            <button
              onClick={() => {
                openEdit(foodEntryItem); /* -> opens FoodEntryForm */
                setFormMode("edit");
              }}
            >
              Edit
            </button>
            <p className="text-sm font-medium text-heading truncate">
              <strong>
                {foodEntryItem.food.name} |
                {(foodEntryItem.food.kcal *
                  (foodEntryItem.food_grams || foodEntryItem.grams)) /
                  100}{" "}
                kcal |{foodEntryItem.food_grams || foodEntryItem.grams} g
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
      ));
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
            /*TODO: make helper function - closeSelector()*/
            setSelectorData(null);
            setFormTarget(null);
          }}
        >
          X
        </button>
      </div>

      <input
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
