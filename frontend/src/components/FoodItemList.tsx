import type { components } from "../types/api";
import { api } from "../api/client.ts";

type FoodOut = components["schemas"]["FoodOut"];

type FoodListItemProps = {
  foodData: components["schemas"]["FoodEntryOut-Output"][];
  fetchFoodData: () => Promise<void>;
  setFoodEntryFormData: (arg: FoodOut) => void;
  setFoodEntryFormVisible: (arg: boolean) => void;
  setFormMode: (arg: "add" | "edit") => void;
  setExistingGrams: (arg: number) => void;
  setFoodEntryItemID: (arg: string) => void;
};

/* 
TODO:       
    consider adding a way to remove food_item elements from a food entry
*/

export default function FoodItemList({
  foodData,
  fetchFoodData,
  setFoodEntryFormData,
  setFoodEntryFormVisible,
  setFormMode,
  setExistingGrams,
  setFoodEntryItemID,
}: FoodListItemProps) {
  /*
    TODO:
        add functionality for removing and editing food entries
        create api methods to handle it
    */
  const foodRows = foodData.map((foodEntry) => (
    <tr>
      <td className="px-4 py-4 text-sm font-medium whitespace-nowrap">
        <div className="inline bg-emerald-100/60 dark:bg-gray-800">
          <p className="text-sm font-normal text-gray-600 dark:text-gray-400">
            <button
              onClick={() => {
                /*                             
                                For future, add food item selector for recipes here
                            */
                const FoodEntryItem = foodEntry.food_items[0];
                setFormMode("edit");
                setFoodEntryFormData(FoodEntryItem.food);
                setFoodEntryItemID(FoodEntryItem.id);
                setExistingGrams(FoodEntryItem.food_grams);
                setFoodEntryFormVisible(true);
              }}
            >
              Edit
            </button>
          </p>
        </div>
      </td>

      <td className="px-4 py-4 text-sm font-medium whitespace-nowrap">
        <div className="inline bg-emerald-100/60 dark:bg-gray-800">
          <p className="text-sm font-normal text-gray-600 dark:text-gray-400">
            <strong>{foodEntry.name}</strong>
          </p>
        </div>
      </td>

      <td className="px-4 py-4 text-sm font-medium whitespace-nowrap">
        <div className="inline bg-emerald-100/60 dark:bg-gray-800">
          <p className="text-sm font-normal text-gray-600 dark:text-gray-400">
            {foodEntry.food_grams}g
          </p>
        </div>
      </td>

      <td className="px-4 py-4 text-sm font-medium whitespace-nowrap">
        <div className="inline bg-emerald-100/60 dark:bg-gray-800">
          <p className="text-sm font-normal text-gray-600 dark:text-gray-400">
            {foodEntry.kcal}
          </p>
        </div>
      </td>

      <td className="px-4 py-4 text-sm font-medium whitespace-nowrap">
        <div className="inline bg-emerald-100/60 dark:bg-gray-800">
          <p className="text-sm font-normal text-gray-600 dark:text-gray-400">
            {foodEntry.carbs.toFixed(1)}g
          </p>
        </div>
      </td>

      <td className="px-4 py-4 text-sm font-medium whitespace-nowrap">
        <div className="inline bg-emerald-100/60 dark:bg-gray-800">
          <p className="text-sm font-normal text-gray-600 dark:text-gray-400">
            {foodEntry.protein.toFixed(1)}g
          </p>
        </div>
      </td>

      <td className="px-4 py-4 text-sm font-medium whitespace-nowrap">
        <div className="inline bg-emerald-100/60 dark:bg-gray-800">
          <p className="text-sm font-normal text-gray-600 dark:text-gray-400">
            {foodEntry.fat.toFixed(1)}g
          </p>
        </div>
      </td>
      <td className="px-4 py-4 text-sm font-medium whitespace-nowrap">
        <div className="inline bg-emerald-100/60 dark:bg-gray-800">
          <button
            onClick={async () => {
              await api.delete(`/api/food_delete/food_entry/${foodEntry.id}`);
              fetchFoodData();
            }}
          >
            X
          </button>
        </div>
      </td>
    </tr>
  ));

  return (
    <div className="food-item-list">
      <div className="flex flex-col mt-6">
        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden border border-gray-200 dark:border-gray-700 md:rounded-lg">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th
                      scope="col"
                      className="py-3.5 px-4 text-sm font-normal text-center rtl:text-right text-gray-500 dark:text-gray-400"
                    >
                      <span></span>
                    </th>
                    <th
                      scope="col"
                      className="py-3.5 px-4 text-sm font-normal text-center rtl:text-right text-gray-500 dark:text-gray-400"
                    >
                      <span>Food Name</span>
                    </th>
                    <th
                      scope="col"
                      className="py-3.5 px-4 text-sm font-normal text-center rtl:text-right text-gray-500 dark:text-gray-400"
                    >
                      <span>Food amount</span>
                    </th>
                    <th
                      scope="col"
                      className="px-12 py-3.5 text-sm font-normal text-center rtl:text-right text-gray-500 dark:text-gray-400"
                    >
                      kcal
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3.5 text-sm font-normal text-center rtl:text-right text-gray-500 dark:text-gray-400"
                    >
                      Carbs
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3.5 text-sm font-normal text-center rtl:text-right text-gray-500 dark:text-gray-400"
                    >
                      Protein
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3.5 text-sm font-normal text-center rtl:text-right text-gray-500 dark:text-gray-400"
                    >
                      Fats
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3.5 text-sm font-normal text-center rtl:text-right text-gray-500 dark:text-gray-400"
                    ></th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200 dark:divide-gray-700 dark:bg-gray-900">
                  {foodRows}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
