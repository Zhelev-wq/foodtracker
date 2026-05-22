import { useState } from 'react'
import type { components } from '../../../../frontend/src/types/api.ts';
import FoodEntryForm from './FoodEntryForm.tsx'

/*
take in search results
display each search result in its own list item with add button for each
on click bring up form to enter food grams and submit

TODO:
    add button to bring in more results
    wait for change in API to make use of date prop
*/
type FoodOut = components["schemas"]["FoodOut"]
type FoodResultsListProps = {
    foodSearchResults: FoodOut[],
    date: Date
}

export default function FoodResultList({foodSearchResults, date}: FoodResultsListProps) {

    const [foodEntryFormData, setFoodEntryFormData] = useState({});
    
    const formattedSearchResults = foodSearchResults.map((result:FoodOut) => 
        <li className="pb-3 sm:pb-4">
            <div className="flex items-center space-x-4 rtl:space-x-reverse">

                <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-heading truncate">
                    <strong>{result.name}</strong>
                    
                    </p>
                    <p className="text-sm text-body truncate">
                    {result.kcal} kcal | {result.protein} Protein | {result.carbs} Carbs | {result.fat} Fat
                    </p>
                </div>
                <div className="inline-flex items-center text-base font-semibold text-heading">
                    <button onClick={() => setFoodEntryFormData(result)}  >Add</button>
                </div>
            </div>
        </li>
    )

    return (
        <div className="flex items-center justify">
            <ul className="max-w-md divide-y divide-default a border">
                {formattedSearchResults}
            </ul>
            <FoodEntryForm foodEntryFormData={foodEntryFormData} date={date}/>
        </div>
    )
}