import { createContext, useState } from "react";
import { components } from "../../types/api.ts";
import { createFoodEntry, editFoodEntryItem } from "../../api/utils.ts";

type FoodOut = components["schemas"]["FoodOut"];
type FoodEntryItemOut = components["schemas"]["FoodEntryItemOut"];

export const FoodEntryFormContext = createContext(null);

export function FoodEntryFormContextProvider({ children }) {
  const [foodOutData, setFoodOutData] = useState<FoodOut | null>(null);
  const [foodEntryItemID, setFoodEntryItemID] = useState<string | null>(null);
  const [formMode, setFormMode] = useState<
    "add" | "edit" | "edit-single" | null
  >(null);
  const [existingGrams, setExistingGrams] = useState<number>(100);
  const [selectorData, setSelectorData] = useState<FoodEntryItemOut[] | []>(
    [],
  ); /* editing for foodEntries/Recipes happens to this element. once editied, its sent via api call*/
  const [formTarget, setFormTarget] = useState(null); /*  */
  const [foodEntryID, setFoodEntryID] = useState(null);

  const openAdd = (FoodOut: FoodOut) => {
    setFoodOutData(FoodOut);
    setFormMode("add");
    setExistingGrams(100);
  };
  const openEdit = (foodEntryItemOut: FoodEntryItemOut) => {
    setFormMode("edit");
    setFoodOutData(foodEntryItemOut.food);
    setExistingGrams(foodEntryItemOut.food_grams);
    setFoodEntryItemID(foodEntryItemOut.id);
  };
  const openEditSingle = (foodEntryItemOut: FoodEntryItemOut) => {
    /* for single-item foodEntry, pass item directly to foodEntryForm, skip FoodEntryItemSelector step */
    setFoodOutData(foodEntryItemOut.food);
    setExistingGrams(foodEntryItemOut.food_grams);
    setFoodEntryItemID(foodEntryItemOut.id);
    setFormMode("edit-single");
  };
  const closeForm = () => {
    setFoodOutData(null);
    setFormMode(null);
    setFoodEntryItemID(null);
    setExistingGrams(100);
    setFormTarget(null);
  };

  function writeFoodItemEditToSelectorData(
    targetFoodEntryItemID: string,
    grams: number,
  ) {
    const updatedItems = [];
    selectorData.forEach((foodEntryItem: FoodEntryItemOut) => {
      if (foodEntryItem.id === targetFoodEntryItemID) {
        const updatedItem = { ...foodEntryItem };
        updatedItem.food_grams = grams;
        updatedItems.push(updatedItem);
      } else {
        updatedItems.push(foodEntryItem);
      }
    });
    setSelectorData(updatedItems);
  }

  const removeItemFromEntry = (foodEntryItem) => {
    const updatedItems = selectorData.filter(
      (item) => item.id !== foodEntryItem.id,
    );
    setSelectorData(updatedItems);
  };

  const saveEntryToLog = (grams) => {
    if (formMode === "edit-single") {
      editFoodEntryItem(foodEntryItemID, grams);
    } else if (formMode === "add") {
      createFoodEntry(foodOutData.id, grams);
    }
    window.location.reload();
  };

  function pushNewEntryToSelectorData(grams) {
    const newItem = {
      food_uuid: foodOutData.id,
      grams: grams,
      food: foodOutData,
    };
    const updatedItems = selectorData.slice();
    updatedItems.push(newItem);
    setSelectorData(updatedItems);
  }

  function writeDataToEntry(grams) {
    if (formMode == "add") {
      pushNewEntryToSelectorData(grams);
    } else if (formMode === "edit") {
      writeFoodItemEditToSelectorData(foodEntryItemID, grams);
    }
  }

  const submitForm = (e, grams) => {
    e.preventDefault();
    if (formTarget == "daily-log") {
      saveEntryToLog(grams);
    } else if (formTarget == "food-entry") {
      writeDataToEntry(grams);
    }
  };

  const passFoodEntryToForm = (foodEntry) => {
    setFoodEntryID(foodEntry.id);
    if (foodEntry.food_items.length === 1) {
      setFormTarget("daily-log");
      setSelectorData(null);
      openEditSingle(foodEntry.food_items[0]);
    } else {
      setSelectorData(foodEntry.food_items);
    }
  };

  const contextValue = {
    foodOutData: foodOutData,
    foodEntryItemID: foodEntryItemID,
    formMode: formMode,
    existingGrams: existingGrams,
    selectorData: selectorData,
    formTarget: formTarget,
    foodEntryID: foodEntryID,

    setSelectorData: setSelectorData,
    setFormTarget: setFormTarget,
    setFoodEntryID: setFoodEntryID,
    openAdd: openAdd,
    openEdit: openEdit,
    closeForm: closeForm,
    openEditSingle: openEditSingle,
    saveEntryToLog: saveEntryToLog,
    submitForm: submitForm,
    passFoodEntryToForm: passFoodEntryToForm,
    removeItemFromEntry: removeItemFromEntry,
  };

  return (
    <FoodEntryFormContext value={contextValue}>{children}</FoodEntryFormContext>
  );
}
