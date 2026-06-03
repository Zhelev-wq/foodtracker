import type { components } from "../../types/api.ts";
import { useState } from "react";
import { api } from "../../api/client.ts";

type FoodOut = components["schemas"]["FoodOut"];
type FoodEntryFormProps =
  | {
      mode: "add";
      FoodOutData: FoodOut;
      isVisible: boolean;
      setVisible: (arg: boolean) => void;
    }
  | {
      mode: "edit";
      FoodOutData: FoodOut;
      existingGrams: number;
      FoodEntryItemId: string;
      isVisible: boolean;
      setVisible: (arg: boolean) => void;
    };

type AddFoodFormProps = {
  FoodOutData: FoodOut;
  isVisible: boolean;
  setVisible: (arg: boolean) => void;
};

type EditFoodProps = {
  FoodOutData: FoodOut;
  existingGrams: number;
  FoodEntryItemId: string;
  isVisible: boolean;
  setVisible: (arg: boolean) => void;
};

function AddFoodForm({ FoodOutData, setVisible }: AddFoodFormProps) {
  function ProcessData(FoodOutData: FoodOut) {
    if (!FoodOutData) {
      return <p>No data</p>;
    }

    const details = Object.entries(FoodOutData).map((pair) => (
      <li>
        {pair[0]}: {(pair[1] * ratio).toFixed(1) || 0}
      </li>
    ));
    return details;
  }
  const { name, vitamins, minerals, fats, id, barcode, ...macros } =
    FoodOutData;
  const [grams, setGrams] = useState(100);
  const ratio = grams / 100;

  const macrosDetails = ProcessData(macros);
  const vitaminDetails = ProcessData(vitamins);
  const mineralDetails = ProcessData(minerals);
  const fatDetails = ProcessData(fats);

  return (
    <div className="border">
      <h2>Add Food Entry</h2>
      <div className="flex justify-between">
        <h2>{name}</h2>
        <button
          className="bg-red-500 hover:bg-blue-700 text-white font-bold py-2 px-4"
          onClick={() => setVisible(false)}
        >
          X
        </button>
      </div>

      <form>
        <div className="flex">
          <input
            onChange={(e) => setGrams(Number(e.target.value))}
            placeholder="weight"
            className="block w-full p-3 ps-9 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand shadow-xs placeholder:text-body"
            required
          />

          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4"
            onClick={() => {
              api.post("/api/food_create/food_entry", [
                {
                  food_uuid: id,
                  grams: grams,
                },
              ]);
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

function EditFoodForm({
  FoodOutData,
  existingGrams,
  FoodEntryItemId,
  setVisible,
}: EditFoodProps) {
  function ProcessData(FoodOutData: FoodOut) {
    if (!FoodOutData) {
      return <p>No data</p>;
    }

    const details = Object.entries(FoodOutData).map((pair) => (
      <li>
        {pair[0]}: {(pair[1] * ratio).toFixed(1) || 0}
      </li>
    ));
    return details;
  }

  const { name, vitamins, minerals, fats, id, barcode, ...macros } =
    FoodOutData;

  const [grams, setGrams] = useState(existingGrams);
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
          onClick={() => setVisible(false)}
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
            onClick={() => {
              api.patch(`/api/food_edit/food_entry_item/${FoodEntryItemId}`, {
                grams: grams,
              });
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
/*
revised version:
    FoodEntryForm will take two types of input
        direct FoodOut for adding entries 
        unpacked FoodEntryItemOut, containing id, food_id, food_grams, FoodOut, for editing entries
    mode will dictate what api call is sent out 
*/

export default function FoodEntryForm(props: FoodEntryFormProps) {
  const isVisible = props.isVisible;
  const mode = props.mode;
  const FoodOutData = props.FoodOutData;
  const setVisible = props.setVisible;
  if (!isVisible || !FoodOutData) {
    return null;
  }

  if (mode == "edit") {
    const existingGrams = props.existingGrams;
    const FoodEntryItemId = props.FoodEntryItemId;
    return (
      <EditFoodForm
        FoodOutData={FoodOutData}
        setVisible={setVisible}
        existingGrams={existingGrams}
        FoodEntryItemId={FoodEntryItemId}
      />
    );
  }

  return <AddFoodForm FoodOutData={FoodOutData} setVisible={setVisible} />;
}
