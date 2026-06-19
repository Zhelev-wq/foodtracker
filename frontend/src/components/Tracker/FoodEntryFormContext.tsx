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
type FoodEntry = components["schemas"]["FoodEntryOut"];
type Recipe = components["schemas"]["RecipeOut-Output"];
type FoodEntryItemOut = components["schemas"]["FoodEntryItemOut-Output"];
type RecipeEntryItemOut = components["schemas"]["RecipeItemOut-Output"];

export const FoodEntryFormContext = createContext(null);

type props = {
  children: any;
  reload: () => void;
};

export function FoodEntryFormContextProvider({ children, reload }: props) {
  const [foodOutData, setFoodOutData] = useState<FoodOut | null>(null);
  const [foodEntryItemID, setFoodEntryItemID] = useState<string | null>(null);
  const [formMode, setFormMode] = useState<"add" | "edit" | null>(
    null,
  ); /* only set by Add Food / Edit Buttons / Close buttons. used for calling correct api method on submit */
  const [existingGrams, setExistingGrams] = useState<number>(100);
  const [selectorData, setSelectorData] = useState<FoodEntry | Recipe | null>(
    null,
  ); /* editing for foodEntries/Recipes happens to this element. once editied, its sent via api call*/
  const [formTarget, setFormTarget] = useState<"food-entry" | "recipe" | null>(
    null,
  ); /*  */
  const [forDailyLog, setForDailyLog] = useState<boolean>(false);
  const [showSearchBar, setShowSearchBar] = useState<boolean>(false);

  const openAdd = (FoodOut: FoodOut) => {
    setFoodOutData(FoodOut);
    setExistingGrams(100);
  };
  const openEdit = (foodEntryItem: FoodEntryItemOut) => {
    /* TODO: create type for this new struct with localId */
    setFormMode("edit");
    if (forDailyLog) {
      setForDailyLog(false);
    }
    setFoodOutData(foodEntryItem.food);
    setExistingGrams(foodEntryItem.food_grams);
    setFoodEntryItemID(foodEntryItem.food_id);
  };
  const openDirectToForm = (foodEntryItemOut: FoodEntryItemOut) => {
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
    if (forDailyLog) {
      setForDailyLog(false);
      setShowSearchBar(false);
    }
  };

  const foodIdOf = (item: FoodEntryItemOut | RecipeEntryItemOut) =>
    item.food_id ?? item.food_uuid;

  function updateItemInSelector(targetFoodID: string, grams: number) {
    /* changes target item's grams, appends all items to new array, 
    writes new array to selectorData*/

    const withGrams = (item, grams) => {
      const copy = Object.assign({}, item);
      if ("food_grams" in copy) {
        copy.food_grams = grams;
      } else {
        copy.grams = grams;
      }
      return copy;
    };

    const updatedItems = selectorData?.food_items.map((item) => {
      if (foodIdOf(item) === targetFoodID) {
        return withGrams(item, grams);
      }
      return item;
    });

    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.food_items = updatedItems;
    setSelectorData(updatedSelectorData);
  }

  const removeItemFromEntry = (foodEntryItem) => {
    /* returns new array minus target item, writes new array to selectorData */
    const updatedItems = selectorData.food_items.filter(
      (item) => foodIdOf(item) !== foodIdOf(foodEntryItem),
    );
    const updatedSelectorData = Object.assign({}, selectorData);
    updatedSelectorData.food_items = updatedItems;
    setSelectorData(updatedSelectorData);
  };

  const saveEntryToLog = async (grams) => {
    if (formMode === "edit") {
      await editFoodEntryItem(foodEntryItemID, grams);
    } else if (formMode === "add") {
      await createFoodEntry(foodOutData.id, grams);
    }
    reload();
  };

  function pushNewEntryToSelectorData(grams: Number) {
    /* appends new entry to selectorData array 
    newItem fields mismatch RecipeEntryItem model fields. this is intentional
    edit recipe/food_entry has two types of validators - existing items/incoming items
    fields mismatch force existing items into one schema, new items into another
    */
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

  function writeDataToEntry(grams: Number) {
    /* checks if form item exists in entry/recipe
    if yes - updates it with new grams; if no - appends it
    */
    const existing = selectorData.food_items.find(
      (item) => foodIdOf(item) === foodOutData.id,
    );

    if (existing) {
      updateItemInSelector(foodIdOf(existing), grams);
    } else {
      pushNewEntryToSelectorData(grams);
    }
  }

  const submitForm = (e, grams) => {
    e.preventDefault();
    if (forDailyLog) {
      saveEntryToLog(grams);
      setForDailyLog(false);
      closeForm();
      return;
    }

    writeDataToEntry(grams);
  };

  const passFoodEntryToForm = (foodEntry) => {
    setFormMode("edit");
    if (foodEntry.food_items.length === 1) {
      setSelectorData(null);
      openDirectToForm(foodEntry.food_items[0]);
    } else {
      setSelectorData(foodEntry);
      setFormTarget("food-entry");
    }
  };

  async function updateOrCreateRecipe(selectorData) {
    if (formMode === "edit") {
      await editRecipe(selectorData);
    } else if (formMode === "add") {
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

  function closeSelector() {
    setSelectorData(null);
    setFormTarget(null);
  }

  async function saveRecipe() {
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

  function openEditRecipe(recipe) {
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

  return (
    <FoodEntryFormContext value={contextValue}>{children}</FoodEntryFormContext>
  );
}
