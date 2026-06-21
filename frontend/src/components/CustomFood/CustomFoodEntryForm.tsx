import { createCustomFood, editCustomFood } from "../../api/utils";
import { components } from "../../types/api";
import React from "react";

type CustomFoodEntryFormProps = {
  foodOut: components["schemas"]["FoodOutput"] | null;
  formMode: "edit" | "add" | null;
  setFormMode: (arg: "edit" | "add" | null) => void;
  reload: () => void;
};

export default function CustomFoodEntryForm({
  foodOut,
  formMode,
  setFormMode,
  reload,
}: CustomFoodEntryFormProps) {
  if (!(formMode === "edit" || formMode === "add")) {
    return null;
  }

  function formatRawFoodData(rawData: Record<string, FormDataEntryValue>) {
    const vitaminsData = {
      vit_a: Number(rawData.vit_a),
      vit_b1: Number(rawData.vit_b1),
      vit_b2: Number(rawData.vit_b2),
      vit_b3: Number(rawData.vit_b3),
      pantothenic_acid: Number(rawData.pantothenic_acid),
      vit_b6: Number(rawData.vit_b6),
      vit_b7: Number(rawData.vit_b7),
      biotin: Number(rawData.biotin),
      vit_b9: Number(rawData.vit_b9),
      vit_b12: Number(rawData.vit_b12),
      vit_c: Number(rawData.vit_c),
      vit_d: Number(rawData.vit_d),
      vit_e: Number(rawData.vit_e),
      vit_k: Number(rawData.vit_k),
    };
    const mineralsData = {
      calcium: Number(rawData.calcium),
      magnesium: Number(rawData.magnesium),
      phosphorus: Number(rawData.phosphorus),
      sodium: Number(rawData.sodium),
      sulfur: Number(rawData.sulfur),
      iron: Number(rawData.iron),
      zinc: Number(rawData.zinc),
      copper: Number(rawData.copper),
      manganese: Number(rawData.manganese),
      molybdenum: Number(rawData.molybdenum),
      selenium: Number(rawData.selenium),
      iodine: Number(rawData.iodine),
      fluoride: Number(rawData.fluoride),
      chromium: Number(rawData.chromium),
      potassium: Number(rawData.potassium),
      taurine: Number(rawData.taurine),
    };
    const fatsData = {
      saturated_fat: Number(rawData.saturated_fat),
      monounsaturated_fat: Number(rawData.monounsaturated_fat),
      polyunsaturated_fat: Number(rawData.polyunsaturated_fat),
      omega_3_fat: Number(rawData.omega_3_fat),
      omega_6_fat: Number(rawData.omega_6_fat),
      omega_9_fat: Number(rawData.omega_9_fat),
      trans_fat: Number(rawData.trans_fat),
    };

    const formattedData = {
      name: rawData.name,
      barcode: rawData.barcode,
      kcal: Number(rawData.kcal),
      carbs: Number(rawData.carbs),
      protein: Number(rawData.protein),
      fat: Number(rawData.fat),
      alcohol: Number(rawData.alcohol),
      caffeine: Number(rawData.caffeine),
      vitamins: vitaminsData,
      minerals: mineralsData,
      fats: fatsData,
    };
    return formattedData;
  }

  const handleSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const formattedData = formatRawFoodData(Object.fromEntries(fd));
    if (formMode === "add") {
      await createCustomFood(formattedData);
    } else {
      await editCustomFood(formattedData, foodOut?.id);
    }
    reload();
    /* TODO: close form */
  };

  return (
    <div>
      <h2>Create Custom Food</h2>
      <button onClick={() => setFormMode(null)}>X</button>

      <form
        className="flex flex-col gap-3 max-w-md"
        key={foodOut?.id ?? "new"}
        onSubmit={handleSubmit}
      >
        {/* --- identity (always visible) --- */}
        <label>
          Name{" "}
          <input
            name="name"
            defaultValue={foodOut?.name}
            type="text"
            required
          />
        </label>
        <label>
          Barcode{" "}
          <input name="barcode" defaultValue={foodOut?.barcode} type="text" />
        </label>

        {/* --- macros --- */}
        <details open>
          <summary className="cursor-pointer font-medium">Macros</summary>
          <div className="flex flex-col gap-2 pt-2">
            <label>
              kcal{" "}
              <input
                name="kcal"
                defaultValue={foodOut?.kcal ?? 0}
                type="number"
                step="any"
                required
              />
            </label>
            <label>
              Carbs (g){" "}
              <input
                name="carbs"
                defaultValue={foodOut?.carbs ?? 0}
                type="number"
                step="any"
                required
              />
            </label>
            <label>
              Protein (g)
              <input
                name="protein"
                defaultValue={foodOut?.protein ?? 0}
                type="number"
                step="any"
                required
              />
            </label>
            <label>
              Fat (g){" "}
              <input
                name="fat"
                defaultValue={foodOut?.fat ?? 0}
                type="number"
                step="any"
                required
              />
            </label>
            <label>
              Alcohol{" "}
              <input
                name="alcohol"
                defaultValue={foodOut?.alcohol ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Caffeine{" "}
              <input
                name="caffeine"
                defaultValue={foodOut?.caffeine ?? 0}
                type="number"
                step="any"
              />
            </label>
          </div>
        </details>

        {/* --- fats --- */}
        <details>
          <summary className="cursor-pointer font-medium">Fats</summary>
          <div className="flex flex-col gap-2 pt-2">
            <label>
              Saturated{" "}
              <input
                name="saturated_fat"
                defaultValue={foodOut?.fats?.saturated_fat ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Monounsaturated{" "}
              <input
                name="monounsaturated_fat"
                defaultValue={foodOut?.fats?.monounsaturated_fat ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Polyunsaturated{" "}
              <input
                name="polyunsaturated_fat"
                defaultValue={foodOut?.fats?.polyunsaturated_fat ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Omega-3{" "}
              <input
                name="omega_3_fat"
                defaultValue={foodOut?.fats?.omega_3_fat ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Omega-6{" "}
              <input
                name="omega_6_fat"
                defaultValue={foodOut?.fats?.omega_6_fat ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Omega-9{" "}
              <input
                name="omega_9_fat"
                defaultValue={foodOut?.fats?.omega_9_fat ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Trans{" "}
              <input
                name="trans_fat"
                defaultValue={foodOut?.fats?.trans_fat ?? 0}
                type="number"
                step="any"
              />
            </label>
          </div>
        </details>

        {/* --- vitamins --- */}
        <details>
          <summary className="cursor-pointer font-medium">Vitamins</summary>
          <div className="flex flex-col gap-2 pt-2">
            <label>
              Vitamin A{" "}
              <input
                name="vit_a"
                defaultValue={foodOut?.vitamins?.vit_a ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              B1 (Thiamin){" "}
              <input
                name="vit_b1"
                defaultValue={foodOut?.vitamins?.vit_b1 ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              B2 (Riboflavin){" "}
              <input
                name="vit_b2"
                defaultValue={foodOut?.vitamins?.vit_b2 ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              B3 (Niacin){" "}
              <input
                name="vit_b3"
                defaultValue={foodOut?.vitamins?.vit_b3 ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              B5 (Pantothenic){" "}
              <input
                name="pantothenic_acid"
                defaultValue={foodOut?.vitamins?.pantothenic_acid ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              B6{" "}
              <input
                name="vit_b6"
                defaultValue={foodOut?.vitamins?.vit_b6 ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              B7{" "}
              <input
                name="vit_b7"
                defaultValue={foodOut?.vitamins?.vit_b7 ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Biotin (B8){" "}
              <input
                name="biotin"
                defaultValue={foodOut?.vitamins?.biotin ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              B9 (Folate){" "}
              <input
                name="vit_b9"
                defaultValue={foodOut?.vitamins?.vit_b9 ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              B12{" "}
              <input
                name="vit_b12"
                defaultValue={foodOut?.vitamins?.vit_b12 ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Vitamin C{" "}
              <input
                name="vit_c"
                defaultValue={foodOut?.vitamins?.vit_c ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Vitamin D{" "}
              <input
                name="vit_d"
                defaultValue={foodOut?.vitamins?.vit_d ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Vitamin E{" "}
              <input
                name="vit_e"
                defaultValue={foodOut?.vitamins?.vit_e ?? 0}
                type="number"
                step="any"
              />
            </label>
            <label>
              Vitamin K{" "}
              <input
                name="vit_k"
                defaultValue={foodOut?.vitamins?.vit_k ?? 0}
                type="number"
                step="any"
              />
            </label>
          </div>
        </details>

        {/* --- minerals --- */}
        <details>
          <summary className="cursor-pointer font-medium">Minerals</summary>
          <div className="flex flex-col gap-2 pt-2">
            <label>
              Calcium{" "}
              <input
                name="calcium"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.calcium ?? 0}
              />
            </label>
            <label>
              Magnesium{" "}
              <input
                name="magnesium"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.magnesium ?? 0}
              />
            </label>
            <label>
              Phosphorus{" "}
              <input
                name="phosphorus"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.phosphorus ?? 0}
              />
            </label>
            <label>
              Sodium{" "}
              <input
                name="sodium"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.sodium ?? 0}
              />
            </label>
            <label>
              Sulfur{" "}
              <input
                name="sulfur"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.sulfur ?? 0}
              />
            </label>
            <label>
              Iron{" "}
              <input
                name="iron"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.iron ?? 0}
              />
            </label>
            <label>
              Zinc{" "}
              <input
                name="zinc"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.zinc ?? 0}
              />
            </label>
            <label>
              Copper{" "}
              <input
                name="copper"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.copper ?? 0}
              />
            </label>
            <label>
              Manganese{" "}
              <input
                name="manganese"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.manganese ?? 0}
              />
            </label>
            <label>
              Molybdenum{" "}
              <input
                name="molybdenum"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.molybdenum ?? 0}
              />
            </label>
            <label>
              Selenium{" "}
              <input
                name="selenium"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.selenium ?? 0}
              />
            </label>
            <label>
              Iodine{" "}
              <input
                name="iodine"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.iodine ?? 0}
              />
            </label>
            <label>
              Fluoride{" "}
              <input
                name="fluoride"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.fluoride ?? 0}
              />
            </label>
            <label>
              Chromium{" "}
              <input
                name="chromium"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.chromium ?? 0}
              />
            </label>
            <label>
              Potassium{" "}
              <input
                name="potassium"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.potassium ?? 0}
              />
            </label>
            <label>
              Taurine{" "}
              <input
                name="taurine"
                type="number"
                step="any"
                defaultValue={foodOut?.minerals?.taurine ?? 0}
              />
            </label>
          </div>
        </details>

        <button type="submit">Save Food</button>
        <button>[PLACEHOLDER]Add to Log</button>
      </form>
    </div>
  );
}
