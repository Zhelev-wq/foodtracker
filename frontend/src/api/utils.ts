import { api } from "./client";
import { components } from "../types/api";
import { DraftEntry } from "../types/draft";

type CustomFoodInput = components["schemas"]["CustomFoodInput"];

export async function editFoodEntryItem(
  foodEntryItemID: string,
  grams: number,
) {
  const response = await api.patch(
    `/api/food-entry-items/${foodEntryItemID}`,
    {
      grams: grams,
    },
  );
  const data = response.data;
  return data;
}

export async function createFoodEntry(food_uuid: string, grams: number) {
  const response = await api.post("/api/food-entries", [
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
    `/api/food-entries/${foodEntryID}`,
  );
  const data = response.data;
  return data;
}

export async function getFoodEntriesForDate(date: string) {
  const response = await api.get(`/api/food-entries/${date}`);
  const data = response.data;
  return data;
}

export async function searchFoodByName(searchText: string) {
  const response = await api.get(`/api/foods/${searchText}`);
  const data = response.data;
  return data;
}

export async function getCustomFoods() {
  const response = await api.get(`/api/foods/custom-foods`);
  const data = response.data;
  return data;
}

export async function getRecipes() {
  const response = await api.get(`/api/recipes`);
  const data = response.data;
  return data;
}

export async function createCustomFood(foodData: CustomFoodInput) {
  const response = await api.post(`/api/foods/custom-foods`, foodData);
  const data = response.data;
  return data;
}

export async function editCustomFood(
  foodData: CustomFoodInput,
  food_uuid: string,
) {
  const response = await api.put(
    `/api/foods/custom-foods/${food_uuid}`,
    foodData,
  );
  const data = response.data;
  return data;
}

export async function saveFoodEntryEdit(foodEntry: DraftEntry) {
  const response = await api.put(
    `/api/food-entries/${foodEntry.id}`,
    foodEntry.food_items,
  );
  const data = response.data;
  return data;
}

export async function createRecipe(selectorData: DraftEntry) {
  const payload = {
    food_items: selectorData.food_items,
    name: selectorData.name,
  };

  const response = await api.post(`/api/recipes`, payload);
  return response.data;
}

export async function editRecipe(selectorData: DraftEntry) {
  const payload = {
    food_items: selectorData.food_items,
    name: selectorData.name,
  };

  const response = await api.put(
    `/api/recipes/${selectorData.id}`,
    payload,
  );
  return response.data;
}

export async function addRecipeToLog(recipe_id: string) {
  const response = await api.post(
    `/api/recipes/${recipe_id}/food-entries`,
  );
  const data = response.data;

  return data;
}

export async function deleteRecipe(recipe_id: string) {
  const response = await api.delete(`/api/recipes/${recipe_id}`);
  const data = response.data;
  return data;
}
