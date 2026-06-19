import { useContext } from "react";
import { FoodEntryFormContext } from "../Tracker/FoodEntryFormContext";

type FoodSearchBarProps = {
  setSearchText: (input: string) => void;
};

export default function FoodSearchBar({ setSearchText }: FoodSearchBarProps) {
  const context = useContext(FoodEntryFormContext);
  if (!context) {
    throw new Error(
      "Component must be used inside FoodEntryFormContextProvider",
    );
  }
  const formTarget = context.formTarget;
  const formMode = context.formMode;
  const showSearchBar = context.showSearchBar;

  if (!formMode || !showSearchBar) {
    return null;
  }

  const Heading = () => {
    if (formTarget === "daily-log") {
      return <h2>Add Food to Daily Log</h2>;
    } else if (formTarget === "food-entry") {
      return <h2>Add Food to Food Entry</h2>;
    } else if (formTarget === "recipe") {
      return <h2>Add Food to Recipe</h2>;
    } else {
      return <h2>Search Food</h2>;
    }
  };

  return (
    <div>
      <Heading />
      <div className="relative">
        <input
          type="search"
          id="search"
          onChange={(e) => setSearchText(e.target.value)}
          className="block w-full p-3 ps-9 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand shadow-xs placeholder:text-body"
          placeholder="Search"
          required
        />
      </div>
    </div>
  );
}
