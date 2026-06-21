import { components } from "./api";

type FoodOutput = components["schemas"]["FoodOutput"];
type FoodEntryItemOutput = components["schemas"]["FoodEntryItemOutput"];
type RecipeItemOutput = components["schemas"]["RecipeItemOutput"];
type NewItem = {
  food_uuid: string;
  grams: number;
  food: FoodOutput;
};

export type DraftItem = FoodEntryItemOutput | RecipeItemOutput | NewItem;
export type DraftEntry = {
  id?: string;
  name?: string | null;
  recipe_name?: string;
  food_items: DraftItem[];
};
