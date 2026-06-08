import { createContext, useState } from "react";
import { components } from "../types/api.ts";

type FoodOut = components["schemas"]["FoodOut"];
type FoodEntryItemOut = components["schemas"]["FoodEntryItemOut"];

export const FoodEntryFormContext = createContext(null);

export function FoodEntryFormContextProvider({ children }) {
  const [foodOutData, setFoodOutData] = useState<FoodOut | null>(null);
  const [foodEntryItemID, setFoodEntryItemID] = useState<string | null>(null);
  const [formMode, setFormMode] = useState<"add" | "edit" | null>(null);
  const [existingGrams, setExistingGrams] = useState<number>(100);
  const [selectorData, setSelectorData] = useState<FoodEntryItemOut[] | []>([]);

  const openAdd = (FoodOut: FoodOut) => {
    setFoodOutData(FoodOut);
    setFormMode("add");
    setExistingGrams(100);
  };
  const openEdit = (foodEntryItemOut: FoodEntryItemOut) => {
    setFoodOutData(foodEntryItemOut.food);
    setExistingGrams(foodEntryItemOut.food_grams);
    setFoodEntryItemID(foodEntryItemOut.id);
    setFormMode("edit");
  };
  const closeForm = () => {
    setFoodOutData(null);
    setFormMode(null);
    setFoodEntryItemID(null);
    setExistingGrams(100);
  };

  const contextValue = {
    foodOutData: foodOutData,
    foodEntryItemID: foodEntryItemID,
    formMode: formMode,
    existingGrams: existingGrams,
    selectorData: selectorData,

    openAdd: openAdd,
    openEdit: openEdit,
    closeForm: closeForm,
    setSelectorData: setSelectorData,
  };

  return (
    <FoodEntryFormContext value={contextValue}>{children}</FoodEntryFormContext>
  );
}
