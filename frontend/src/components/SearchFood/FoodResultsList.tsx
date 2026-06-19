import React, { useContext } from "react";
import { components } from "../../types/api.ts";
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
  const context = useContext(FoodEntryFormContext);
  if (!context) {
    throw new Error(
      "Component must be used inside FoodEntryFormContextProvider",
    );
  }

  const showSearchBar = context.showSearchBar;
  if (!foodSearchResults || !showSearchBar) {
    return null;
  }

  const openAdd = context.openAdd;

  const formattedSearchResults = foodSearchResults.map((result: FoodOut) => (
    <li key={result.id} className="pb-3 sm:pb-4">
      <div className="flex items-center space-x-4 rtl:space-x-reverse">
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-heading truncate">
            <strong>{result.name}</strong>
          </p>
          <p className="text-sm text-body truncate">
            {result.kcal.toFixed(1)} kcal | {result.protein.toFixed(1)} Protein
            | {result.carbs.toFixed(1)} Carbs | {result.fat.toFixed(1)} Fat
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
