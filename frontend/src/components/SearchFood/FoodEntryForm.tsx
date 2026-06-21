import { useState, useContext } from "react";
import { FoodEntryFormContext } from "../Tracker/FoodEntryFormContext.tsx";

/*
revised version:
    FoodEntryForm will take two types of input
        direct FoodOut for adding entries 
        unpacked FoodEntryItemOut, containing id, food_id, food_grams, FoodOut, for editing entries
          edit_mode will use the raw FoodOut details to visualise the macro/micro
          then send the grams to the FoodEntryItem associated with that food
          this necessesitates sending all 4 details separate until a better solution is found
    mode will dictate what api call is sent out 
*/

export default function FoodEntryForm() {
  const context = useContext(FoodEntryFormContext);
  if (!context) {
    throw new Error(
      "Component must be used inside FoodEntryFormContextProvider",
    );
  }
  const existingGrams = context.existingGrams;
  const foodOutData = context.foodOutData;
  const formMode = context.formMode;

  const [grams, setGrams] = useState(existingGrams);

  if (!foodOutData || !formMode) {
    return null;
  }
  const closeForm = context.closeForm;
  const submitForm = context.submitForm;

  function ProcessData(data: Record<string, number | null> | null) {
    if (!data) {
      return <p>No data</p>;
    }

    const details = Object.entries(data).map((pair) => (
      <li>
        {pair[0]}: {((pair[1] ?? 0) * ratio).toFixed(1)}
      </li>
    ));
    return details;
  }

  const { name, vitamins, minerals, fats, id, barcode, user_id, ...macros } =
    foodOutData;

  const ratio = grams / 100;

  const macrosDetails = ProcessData(macros);
  const vitaminDetails = ProcessData(vitamins);
  const mineralDetails = ProcessData(minerals);
  const fatDetails = ProcessData(fats);

  return (
    <div className="border">
      <h2>Edit Food Entry</h2>
      <div className="flex justify-between">
        <h2>{name}</h2>
        <button
          className="bg-red-500 hover:bg-blue-700 text-white font-bold py-2 px-4"
          onClick={() => closeForm()}
        >
          X
        </button>
      </div>

      <form>
        <div className="flex ">
          <input
            onChange={(e) => setGrams(Number(e.target.value))}
            placeholder="weight"
            className="block w-full p-3 ps-9 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand shadow-xs placeholder:text-body"
            required
          />

          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4"
            onClick={(e) => {
              submitForm(e, grams);
            }}
          >
            Save Entry
          </button>
        </div>
        <h3>Macros</h3>
        <ul className="col2">{macrosDetails}</ul>
        <br></br>

        <h3>Vitamins</h3>
        <ul>{vitaminDetails}</ul>
        <br></br>

        <h3>Minerals</h3>
        <ul>{mineralDetails}</ul>

        <br></br>

        <h3>Fats</h3>
        <ul>{fatDetails}</ul>
      </form>
    </div>
  );
}
