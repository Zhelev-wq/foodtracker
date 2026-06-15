import { createContext, useState } from "react";
import { components } from "../../types/api.ts";
import {
  createFoodEntry,
  createRecipe,
  editFoodEntryItem,
  saveFoodEntryEdit,
  editRecipe,
} from "../../api/utils.ts";

type FoodOut = components["schemas"]["FoodOut"];
type FoodEntry = components["schemas"]["FoodEntry"];
type Recipe = null; /* placeholder */
type FoodEntryItemOut = components["schemas"]["FoodEntryItemOut"];

export const FoodEntryFormContext = createContext(null);

export function FoodEntryFormContextProvider({ children }) {
  const [foodOutData, setFoodOutData] = useState<FoodOut | null>(null);
  const [foodEntryItemID, setFoodEntryItemID] = useState<string | null>(null);
  const [formMode, setFormMode] = useState<
    "add" | "edit" | null
  >(null);  /* only set by Add Food / Edit Buttons / Close buttons. used for calling correct api method on submit */
  const [existingGrams, setExistingGrams] = useState<number>(100);
  const [selectorData, setSelectorData] = useState<FoodEntry | Recipe | null>(
    null,
  ); /* editing for foodEntries/Recipes happens to this element. once editied, its sent via api call*/
  const [formTarget, setFormTarget] = useState<
    "food-entry" | "recipe" | null
  >(null); /*  */
  const [forDailyLog, setForDailyLog] = useState<boolean>(false);
  const [showSearchBar, setShowSearchBar] = useState<boolean>(false);

  const openAdd = (FoodOut: FoodOut) => {
    setFoodOutData(FoodOut);
    setExistingGrams(100);
  };
  const openEdit = (foodEntryItemOut: FoodEntryItemOut) => { /* TODO: create type for this new struct with localId */
    setFormMode("edit");
    setFoodOutData(foodEntryItemOut.food);
    setExistingGrams(foodEntryItemOut.food_grams);
    setFoodEntryItemID(foodEntryItemOut.food_id);
  };
  const openEditSingle = (foodEntryItemOut: FoodEntryItemOut) => {
    /* for single-item foodEntry, pass item directly to foodEntryForm, 
      skip FoodEntryItemSelector step,
      used to pass DailyLog entries  */
    setForDailyLog(true);
    setFormMode("edit");
    setFoodOutData(foodEntryItemOut.food);
    setExistingGrams(foodEntryItemOut.food_grams);
    setFoodEntryItemID(foodEntryItemOut.id);
  };
  const closeForm = () => {
    setFoodOutData(null);
    setFoodEntryItemID(null);
    setExistingGrams(100);    
    /*
    setFormMode(null);
    setFormTarget(null);
    */
  };

  function updateItemInSelector(
    targetFoodEntryItemID: string,
    grams: number,
  ) {
    /* changes target item's grams, appends all items to new array, 
    writes new array to selectorData*/
    const updatedItems = [];
    selectorData.food_items.forEach((foodEntryItem: FoodEntryItemOut) => {

      if (foodEntryItem.id === targetFoodEntryItemID) {
        const updatedItem = { ...foodEntryItem };
        updatedItem.food_grams = grams;
        updatedItems.push(updatedItem);
      } 
      else {
        updatedItems.push(foodEntryItem);
      }
    });
    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.food_items = updatedItems;
    setSelectorData(updatedSelectorData);
  }

  const removeItemFromEntry = (foodEntryItem) => {
    /* returns new array minus target item, writes new array to selectorData */
    const updatedItems = selectorData.food_items.filter(
      (item) => item.food_id !== foodEntryItem.food_id,
    );
    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.food_items = updatedItems;
    setSelectorData(updatedSelectorData);
  };

  const saveEntryToLog = (grams) => {
    /* TODO: figure out what this does, rename as necessary */
    if (formMode === "edit") {
      editFoodEntryItem(foodEntryItemID, grams);
    } else if (formMode === "add") {
      createFoodEntry(foodOutData.id, grams);
    }
    window.location.reload();
  };

  function pushNewEntryToSelectorData(grams) {
    /* appends new entry to selectorData array */
    const newItem = {
      food_uuid: foodOutData.id,
      grams: grams,
      food: foodOutData,
    };
    const updatedItems = selectorData.food_items.slice();
    updatedItems.push(newItem);
    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.food_items = updatedItems;
    setSelectorData(updatedSelectorData);      
    }
  

  function writeDataToEntry(grams) {
    /* checks if form item exists in entry/recipe
    if yes - updates it with new grams; if no - appends it
    */
    const existing = selectorData.food_items.find(
      (item) => item.food_id === foodOutData.id
    )

    if (existing) {
      updateItemInSelector(existing.id, grams)
    } else {
      pushNewEntryToSelectorData(grams);
    }
  }

  const submitForm = (e, grams) => {
    e.preventDefault();
    if (forDailyLog) {
      saveEntryToLog(grams);
      return;
    } 

    writeDataToEntry(grams);

    console.log(`FormTarget: ${formTarget}`)
    console.log(`SelectorData: ${JSON.stringify(selectorData)}`);
    console.log(`FormMode: ${formMode}`)
  };

  const passFoodEntryToForm = (foodEntry) => {
    setFormMode("edit")
    if (foodEntry.food_items.length === 1) {
      setSelectorData(null);
      openEditSingle(foodEntry.food_items[0]);
    } else {
      setSelectorData(foodEntry);
      setFormTarget("food-entry")
    }
  };

  async function updateOrCreateRecipe(selectorData) {
    if (formMode==="edit") {
      await editRecipe(selectorData);
    } else if (formMode==="add") {
      await createRecipe(selectorData);
    }
  }

  const commitFoodComposition = async () => {
    if (formTarget === "food-entry") {
      await saveFoodEntryEdit(selectorData); /* this never triggers*/
    } else if (formTarget === "recipe") {
      await updateOrCreateRecipe(selectorData);
    }
  };

  const setRecipeName = (name) => {
    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.recipe_name = name;
    setSelectorData(updatedSelectorData);
  };

  const contextValue = {
    foodOutData: foodOutData,
    foodEntryItemID: foodEntryItemID,
    formMode: formMode,
    existingGrams: existingGrams,
    selectorData: selectorData,
    formTarget: formTarget,
    forDailyLog: forDailyLog,
    showSearchBar: showSearchBar,

    setSelectorData: setSelectorData,
    setFormTarget: setFormTarget,
    openAdd: openAdd,
    openEdit: openEdit,
    closeForm: closeForm,
    openEditSingle: openEditSingle,
    saveEntryToLog: saveEntryToLog,
    submitForm: submitForm,
    passFoodEntryToForm: passFoodEntryToForm,
    removeItemFromEntry: removeItemFromEntry,
    commitFoodComposition: commitFoodComposition,
    setRecipeName: setRecipeName,
    setFormMode: setFormMode,
    setForDailyLog: setForDailyLog,
    setShowSearchBar: setShowSearchBar,
  };

  return (
    <FoodEntryFormContext value={contextValue}>{children}</FoodEntryFormContext>
  );
}
