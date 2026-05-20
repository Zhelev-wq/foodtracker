import { addDays, subDays } from 'date-fns';
import axios from 'axios';
import FoodItemList from './FoodItemList';

export default function DateSelector({date, setDate}) {

    function addDate() {
        const newDate = addDays(date, 1);
        setDate(newDate);
    }

    function subDate() {
        const newDate = subDays(date, 1);
        setDate(newDate);
    }       
        /*
        TODO:
        this should have a visual calendar element 
        which allows us to click on specific dates rather than just doing -+1
        */
    return (
        <div className="date-selector">
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
                onClick={subDate}>-1</button>
            <p>{date.toISOString()}</p>
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
            onClick={addDate}>+1</button>
        </div>
    );
}

