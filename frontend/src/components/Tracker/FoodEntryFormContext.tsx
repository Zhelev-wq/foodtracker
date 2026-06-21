import React, { createContext, useState } from "react";
import { components } from "../../types/api.ts";
import {
  createFoodEntry,
  createRecipe,
  editFoodEntryItem,
  saveFoodEntryEdit,
  editRecipe,
} from "../../api/utils.ts";
import { DraftEntry } from "../../types/draft.ts";

type FoodOutput = components["schemas"]["FoodOutput"];
type FoodEntryOutput = components["schemas"]["FoodEntryOutput"];
type RecipeOutput = components["schemas"]["RecipeOutput"];
type FoodEntryItemOutput = components["schemas"]["FoodEntryItemOutput"];
type RecipeItemOutput = components["schemas"]["RecipeItemOutput"];
type NewItem = {
  food_uuid: string;
  grams: number;
  food: FoodOutput;
};

function getContextValue(reload: () => void) {
  const [foodOutData, setFoodOutData] = useState<FoodOutput | null>(null);
  const [foodEntryItemID, setFoodEntryItemID] = useState<string | null>(null);
  const [formMode, setFormMode] = useState<"add" | "edit" | null>(
    null,
  ); /* only set by Add Food / Edit Buttons / Close buttons. used for calling correct api method on submit */
  const [existingGrams, setExistingGrams] = useState<number>(100);
  const [selectorData, setSelectorData] = useState<DraftEntry | null>(
    null,
  ); /* editing for foodEntries/Recipes happens to this element. once editied, its sent via api call*/
  const [formTarget, setFormTarget] = useState<"food-entry" | "recipe" | null>(
    null,
  ); /*  */
  const [forDailyLog, setForDailyLog] = useState<boolean>(false);
  const [showSearchBar, setShowSearchBar] = useState<boolean>(false);

  const openAdd = (FoodOut: FoodOutput) => {
    setFoodOutData(FoodOut);
    setExistingGrams(100);
  };
  const openEdit = (foodEntryItemOutput: FoodEntryItemOutput) => {
    setFormMode("edit");
    if (forDailyLog) {
      setForDailyLog(false);
    }
    setFoodOutData(foodEntryItemOutput.food);
    setExistingGrams(foodEntryItemOutput.food_grams);
  };
  const openDirectToForm = (foodEntryItemOutput: FoodEntryItemOutput) => {
    /* for single-item foodEntry, pass item directly to foodEntryForm, 
      skip FoodEntryItemSelector step,
      used to pass DailyLog entries  */
    setForDailyLog(true);
    setFormMode("edit");
    setFoodOutData(foodEntryItemOutput.food);
    setExistingGrams(foodEntryItemOutput.food_grams);
    setFoodEntryItemID(foodEntryItemOutput.id); // sent to editFoodEntryItem api call
  };
  const closeForm = () => {
    setFoodOutData(null);
    setFoodEntryItemID(null);
    setExistingGrams(100);
    if (forDailyLog) {
      setForDailyLog(false);
      setShowSearchBar(false);
    }
  };

  const foodIdOf = (item: FoodEntryItemOutput | RecipeItemOutput | NewItem) => {
    if ("food_id" in item) {
      return item.food_id;
    }
    return item.food_uuid;
  };

  function updateItemInSelector(targetFoodID: string, grams: number) {
    /* changes target item's grams, appends all items to new array, 
    writes new array to selectorData*/
    if (!selectorData) {
      throw new Error(
        "selectorData is null when accessed by updateItemInSelector",
      );
    }
    const withGrams = (
      item: FoodEntryItemOutput | RecipeItemOutput | NewItem,
      grams: number,
    ) => {
      const copy = Object.assign({}, item);
      if ("food_grams" in copy) {
        copy.food_grams = grams;
      } else {
        copy.grams = grams;
      }
      return copy;
    };

    const updatedItems = selectorData.food_items.map(
      (item: FoodEntryItemOutput | RecipeItemOutput | NewItem) => {
        if (foodIdOf(item) === targetFoodID) {
          return withGrams(item, grams);
        }
        return item;
      },
    );

    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.food_items = updatedItems;
    setSelectorData(updatedSelectorData);
  }

  const removeItemFromEntry = (
    foodEntryItem: FoodEntryItemOutput | RecipeItemOutput | NewItem,
  ) => {
    /* returns new array minus target item, writes new array to selectorData */
    if (!selectorData) {
      throw new Error(
        "selectorData attr empty when accessed by removeItemFrontEntry",
      );
    }
    const updatedItems = selectorData.food_items.filter(
      (item) => foodIdOf(item) !== foodIdOf(foodEntryItem),
    );
    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.food_items = updatedItems;
    setSelectorData(updatedSelectorData);
  };

  const saveEntryToLog = async (grams: number) => {
    
    if (formMode === "edit" && foodEntryItemID) {
      await editFoodEntryItem(foodEntryItemID, grams);
    } else if (formMode === "add" && foodOutData) {
      await createFoodEntry(foodOutData.id, grams);
    } else {
      throw new Error(
        "foodEntryItemID or foodOutData empty when accessed by saveEntryToLog",
      );
    }
    reload();
  };

  function pushNewEntryToSelectorData(grams: number) {
    /* appends new entry to selectorData array 
    newItem fields mismatch RecipeEntryItem model fields. this is intentional
    edit recipe/food_entry has two types of validators - existing items/incoming items
    fields mismatch force existing items into one schema, new items into another
    */
    if (!selectorData || !foodOutData) {
      throw new Error(
        "selectorData or foodOutData empty when accessed by pushNewEntryToSelectorData",
      );
    }
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

  function writeDataToEntry(grams: number) {
    /* checks if form item exists in entry/recipe
    if yes - updates it with new grams; if no - appends it
    */
    if (!selectorData || !foodOutData) {
      throw new Error(
        "selectorData or foodOutData empty when accessed by writeDataToEntry",
      );
    }
    const existing = selectorData.food_items.find(
      (item) => foodIdOf(item) === foodOutData.id,
    );

    if (existing) {
      updateItemInSelector(foodIdOf(existing), grams);
    } else {
      pushNewEntryToSelectorData(grams);
    }
  }

  const submitForm = (e: React.SyntheticEvent, grams: number) => {
    e.preventDefault();
    if (forDailyLog) {
      saveEntryToLog(grams);
      setForDailyLog(false);
      closeForm();
      return;
    }

    writeDataToEntry(grams);
  };

  const passFoodEntryToForm = (foodEntry: FoodEntryOutput) => {
    setFormMode("edit");
    if (foodEntry.food_items.length === 1) {
      setSelectorData(null);
      openDirectToForm(foodEntry.food_items[0]);
    } else {
      setSelectorData(foodEntry);
      setFormTarget("food-entry");
    }
  };

  async function updateOrCreateRecipe(selectorData: DraftEntry) {
    if (formMode === "edit") {
      await editRecipe(selectorData);
    } else if (formMode === "add") {
      await createRecipe(selectorData);
    }
  }

  const commitFoodComposition = async () => {
    if (!selectorData) {
      throw new Error(
        "selectorData is null when accessed by commitFoodComposition",
      );
    }
    if (formTarget === "food-entry") {
      await saveFoodEntryEdit(selectorData); /* this never triggers*/
    } else if (formTarget === "recipe") {
      await updateOrCreateRecipe(selectorData);
    }
  };

  const setRecipeName = (name: string) => {
    /* TODO: I have no idea what this does or why its here */
    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.recipe_name = name;
    setSelectorData(updatedSelectorData);
  };

  function closeSelector() {
    setSelectorData(null);
    setFormTarget(null);
  }

  async function saveRecipe() {
    if (!selectorData) {
      throw new Error("selectorData is null when accessed by saveRecipe");
    }
    if (formTarget === "recipe") {
      await commitFoodComposition();
    } else if (formTarget === "food-entry") {
      await saveFoodEntryEdit(selectorData);
    }
    reload?.();
    closeForm();
    setShowSearchBar(false);
    setSelectorData(null);
  }

  function openNewEmptyRecipe() {
    setSelectorData({ food_items: [], recipe_name: "" });
    setFormTarget("recipe");
    setFormMode("add");
  }

  function openEditRecipe(recipe: RecipeOutput) {
    setSelectorData(recipe);
    setFormTarget("recipe");
    setFormMode("edit");
  }
  function openNewEntryToLog() {
    setSelectorData(null);
    setForDailyLog(true);
    setFormMode("add");
    setFormTarget("food-entry");
    setShowSearchBar(true);
  }
  const contextValue = {
    showSearchBar: showSearchBar,
    formMode: formMode,
    existingGrams: existingGrams,
    foodOutData: foodOutData,
    selectorData: selectorData,
    formTarget: formTarget,

    setRecipeName: setRecipeName,
    setShowSearchBar: setShowSearchBar,

    /* HELPER FUNCTIONS */
    openAdd: openAdd,
    openEdit: openEdit,
    openEditRecipe: openEditRecipe,
    closeForm: closeForm,
    submitForm: submitForm,
    passFoodEntryToForm: passFoodEntryToForm,
    removeItemFromEntry: removeItemFromEntry,
    foodIdOf: foodIdOf,
    closeSelector: closeSelector,
    saveRecipe: saveRecipe,
    openNewEmptyRecipe: openNewEmptyRecipe,
    openNewEntryToLog: openNewEntryToLog,
  };
  return contextValue;
}

type FoodEntryFormContextValue = ReturnType<typeof getContextValue>;
export const FoodEntryFormContext =
  createContext<FoodEntryFormContextValue | null>(null);

type props = {
  children: any;
  reload: () => void;
};

export function FoodEntryFormContextProvider({ children, reload }: props) {
  const contextValue = getContextValue(reload);
  return (
    <FoodEntryFormContext value={contextValue}>{children}</FoodEntryFormContext>
  );
}
