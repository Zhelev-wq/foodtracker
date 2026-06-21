import { components } from "../../types/api";

type FoodListItemProps = {
  foodData: components["schemas"]["FoodEntryOutput"][];
};

export default function FoodSummary({ foodData }: FoodListItemProps) {
  const foodMacros = {
    kcal: 0,
    protein: 0,
    fat: 0,
    carbs: 0,
  };

  foodData.forEach((foodItem) => {
    foodMacros.kcal += foodItem.kcal;
    foodMacros.protein += foodItem.protein;
    foodMacros.fat += foodItem.fat;
    foodMacros.carbs += foodItem.carbs;
  });

  return (
    <div>
      <h2>Daily Summary</h2>
      <ul>
        <li>KCAL: {foodMacros.kcal}</li>
        <li>Protein: {foodMacros.protein}</li>
        <li>Fat: {foodMacros.fat}</li>
        <li>Carbs: {foodMacros.carbs}</li>
      </ul>
    </div>
  );
}
