import { useContext } from "react";
import type { components } from "../../../../frontend/src/types/api.ts";
import { FoodEntryFormContext } from "../Tracker/FoodEntryFormContext.tsx";

/*
take in search results
display each search result in its own list item with add button for each
on click bring up form to enter food grams and submit

*/
type FoodOut = components["schemas"]["FoodOut"];
type FoodResultsListProps = {
  foodSearchResults: FoodOut[] | null;
};

export default function FoodResultList({
  foodSearchResults,
}: FoodResultsListProps) {
  if (!foodSearchResults) {
    return null;
  }

  const foodEntryFormContext = useContext(FoodEntryFormContext);
  const openAdd = foodEntryFormContext.openAdd;

  const formattedSearchResults = foodSearchResults.map((result: FoodOut) => (
    <li key={result.id} className="pb-3 sm:pb-4">
      <div className="flex items-center space-x-4 rtl:space-x-reverse">
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-heading truncate">
            <strong>{result.name}</strong>
          </p>
          <p className="text-sm text-body truncate">
            {result.kcal} kcal | {result.protein} Protein | {result.carbs} Carbs
            | {result.fat} Fat
          </p>
        </div>
        <div className="inline-flex items-center text-base font-semibold text-heading">
          <button
            onClick={() => {
              /* 
              here, show foodentry form with mode "add"
              provide "result" var as value
              */
              openAdd(result);
            }}
          >
            Add
          </button>
        </div>
      </div>
    </li>
  ));

  return (
    <div className="flex items-center">
      <ul className="max-w-md divide-y divide-default a border">
        {formattedSearchResults}
      </ul>
    </div>
  );
}
