import React, { useContext } from "react";

type FoodSearchBarProps = {
  setSearchText: (input: string) => void;
  contextProp: React.Context;
};

export default function FoodSearchBar({
  setSearchText,
  contextProp,
}: FoodSearchBarProps) {
  /* 
    TODO:
        when pressing enter nothing should happen, now it crashes page
    */

  const context = useContext(contextProp);
  const formTarget = context.formTarget;

  if (!formTarget) {
    setSearchText("");
    return null;
  }

  const Heading = () => {
    console.log(formTarget);
    if (formTarget === "daily-log") {
      return <h2>Add Food to Daily Log</h2>;
    } else if (formTarget === "food-entry") {
      return <h2>Add Food to Food Entry</h2>;
    }
  };

  return (
    <div>
      <Heading />
      <form className="max-w-md mx-auto aling-top">
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
      </form>
    </div>
  );
}
