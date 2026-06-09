import { FoodEntryFormContext } from "../Tracker/FoodEntryFormContext.tsx";
import { useContext } from "react";

export default function FoodEntryItemSelector() {
  const foodEntryFormContext = useContext(FoodEntryFormContext);
  const foodEntryItems = foodEntryFormContext.selectorData;
  const setSelectorData = foodEntryFormContext.setSelectorData;

  if (!foodEntryItems || foodEntryItems.length === 0) {
    return null;
  }

  const openEdit = foodEntryFormContext.openEdit;

  const formattedResults = foodEntryItems.map((foodEntryItem) => (
    <li key={foodEntryItem.id} className="pb-3 sm:pb-4">
      <div className="flex items-center space-x-4- rlt:space-x-reverse">
        <p className="text-sm font-medium text-heading truncate">
          <strong>
            {foodEntryItem.food.name} |
            {(foodEntryItem.food.kcal * foodEntryItem.food_grams) / 100} kcal |
            {foodEntryItem.food_grams} g
          </strong>
          <button
            onClick={() => {
              openEdit(foodEntryItem);
              setSelectorData([]);
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
      <div className="flex">
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
    </div>
  );
}
