import { useState, useEffect } from "react";
import CustomFoodEntryForm from "./CustomFoodEntryForm";
import { components } from "../../types/api";
import { getCustomFoods } from "../../api/utils";

type FoodOutput = components["schemas"]["FoodOutput"];

export default function CustomFood() {
  const [customFood, setCustomFood] = useState([]);
  const [reloadTracker, setReloadTracker] = useState(0);

  useEffect(() => {
    const fetchCustomFood = async () => {
      const food = await getCustomFoods();
      setCustomFood(food);
    };
    fetchCustomFood();
  }, [reloadTracker]);

  const reload = () => {
    const count = reloadTracker + 1;
    setReloadTracker(count);
  };

  function openEdit(food: FoodOutput) {
    setFormMode("edit");
    setFoodDetails(food);
  }

  function openAdd() {
    setFormMode("add");
    setFoodDetails(null);
  }

  const [foodDetails, setFoodDetails] = useState<FoodOutput | null>(null);
  const [formMode, setFormMode] = useState<"edit" | "add" | null>(null);

  const formattedResults = customFood?.map((food: FoodOutput) => (
    <li key={food.id} className="pb-3 sm:pb-4">
      <div className="flex items-center space-x-4- rlt:space-x-reverse">
        <p className="text-sm font-medium text-heading truncate">
          <strong>
            {food.name} | {food.kcal} kcal |
          </strong>
          <button
            onClick={() => {
              openEdit(food);
            }}
          >
            Edit
          </button>
        </p>
      </div>
    </li>
  ));

  return (
    <div className="flex">
      <div>
        <button onClick={() => openAdd()}>Create New Custom Food</button>
        <ul className="divide-y divide-default a border">{formattedResults}</ul>
      </div>
      <CustomFoodEntryForm
        foodOut={foodDetails}
        formMode={formMode}
        setFormMode={setFormMode}
        reload={reload}
      />
    </div>
  );
}
