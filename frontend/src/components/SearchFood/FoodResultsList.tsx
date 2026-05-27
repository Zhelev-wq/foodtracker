import { useState } from 'react'
import type { components } from '../../../../frontend/src/types/api.ts';

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
    foodSearchResults: FoodOut[]|null,    
    date: Date,
    setFoodEntryFormData: (arg: FoodOut|null) => void,
    setFoodEntryFormVisible: (arg: boolean) => void,
    setFormMode: (arg: "add"|"edit") => void,    
}

export default function FoodResultList(
    {
        foodSearchResults, 
        date, 
        setFoodEntryFormData, 
        setFoodEntryFormVisible,
        setFormMode,
    }: FoodResultsListProps
) {    
    const [prevFoodData, setPrevFoodData] = useState(foodSearchResults);
    
    if (!foodSearchResults){
        return null;
    }


    if (foodSearchResults !== prevFoodData) {
        if (prevFoodData !== null ){
            const currentIDs = new Set(foodSearchResults.map(r => r.id));
            const isSubset = prevFoodData.every(entry => currentIDs.has(entry.id))
            if (!isSubset) {
                setFoodEntryFormVisible(false);
            }   
        } 
        setPrevFoodData(foodSearchResults);

    }

    const formattedSearchResults = foodSearchResults.map((result:FoodOut) => 
        <li key={result.id} className="pb-3 sm:pb-4">
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
                    <button onClick={() => {
                        setFormMode("add"); 
                        setFoodEntryFormData(result); 
                        setFoodEntryFormVisible(true);                        
                        }}  >Add</button>
                </div>
            </div>
        </li>
    )

    return (
        <div className="flex items-center">
            <ul className="max-w-md divide-y divide-default a border">
                {formattedSearchResults}
            </ul>
        </div>
    )
}