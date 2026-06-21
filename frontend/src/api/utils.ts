import { api } from "./client";
import { components } from "../types/api";
import { DraftEntry } from "../types/draft";

type CustomFoodInput = components["schemas"]["CustomFoodInput"];

export async function editFoodEntryItem(
  foodEntryItemID: string,
  grams: number,
) {
  const response = await api.patch(
    `/api/food_edit/food_entry_item/${foodEntryItemID}`,
    {
      grams: grams,
    },
  );
  const data = response.data;
  return data;
}

export async function createFoodEntry(food_uuid: string, grams: number) {
  const response = await api.post("/api/food_create/food_entry", [
    {
      food_uuid: food_uuid,
      grams: grams,
    },
  ]);
  const data = response.data;
  return data;
}

export async function deleteFoodEntry(foodEntryID: string) {
  const response = await api.delete(
    `/api/food_delete/food_entry/${foodEntryID}`,
  );
  const data = response.data;
  return data;
}

export async function getFoodEntriesForDate(date: string) {
  const response = await api.get(`/api/food_get/search/date/${date}`);
  const data = response.data;
  return data;
}

export async function searchFoodByName(searchText: string) {
  const response = await api.get(`/api/food_get/search/name/${searchText}`);
  const data = response.data;
  return data;
}

export async function getCustomFoods() {
  const response = await api.get(`/api/food_get/search/custom_food`);
  const data = response.data;
  return data;
}

export async function getRecipes() {
  const response = await api.get(`/api/food_get/search/recipes`);
  const data = response.data;
  return data;
}

export async function createCustomFood(foodData: CustomFoodInput) {
  const response = await api.post(`/api/food_create/custom_food`, foodData);
  const data = response.data;
  return data;
}

export async function editCustomFood(
  foodData: CustomFoodInput,
  food_uuid: string,
) {
  const response = await api.put(
    `/api/food_edit/custom_food/${food_uuid}`,
    foodData,
  );
  const data = response.data;
  return data;
}

export async function saveFoodEntryEdit(foodEntry: DraftEntry) {
  const response = await api.put(
    `/api/food_edit/food_entry/${foodEntry.id}`,
    foodEntry.food_items,
  );
  const data = response.data;
  return data;
}

export async function createRecipe(selectorData: DraftEntry) {
  const payload = {
    food_items: selectorData.food_items,
    recipe_name: selectorData.recipe_name,
  };

  const response = await api.post(`/api/food_create/recipe`, payload);
  return response.data;
}

export async function editRecipe(selectorData: DraftEntry) {
  const payload = {
    food_items: selectorData.food_items,
    recipe_name: selectorData.recipe_name,
  };

  const response = await api.put(
    `/api/food_edit/recipe/${selectorData.id}`,
    payload,
  );
  return response.data;
}

export async function addRecipeToLog(recipe_id: string) {
  const response = await api.post(
    `/api/food_create/entry_from_recipe/${recipe_id}`,
  );
  const data = response.data;

  return data;
}

export async function deleteRecipe(recipe_id: string) {
  const response = await api.delete(`/api/food_delete/recipe/${recipe_id}`);
  const data = response.data;
  return data;
}
