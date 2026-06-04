import { api } from "./client";

export async function editFoodEntry(foodEntryItemID: string, grams: number) {
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

export async function getFoodEntriesForDate(date) {
  const response = await api.get(`/api/food_get/search/date/${date}`);
  const data = response.data;
  return data;
}

export async function searchFoodByName(searchText: string) {
  const response = await api.get(`/api/food_get/search/name/${searchText}`);
  const data = response.data;
  return data;
}
