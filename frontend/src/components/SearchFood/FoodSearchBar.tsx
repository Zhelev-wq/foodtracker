type FoodSearchBarProps = {
  setSearchText: (input: string) => void;
};

export default function FoodSearchBar({ setSearchText }: FoodSearchBarProps) {
  /* 
    TODO:
        when pressing enter nothing should happen, now it crashes page
    */
  return (
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
  );
}
