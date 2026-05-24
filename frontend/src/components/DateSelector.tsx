import { addDays, subDays } from 'date-fns';
import Calendar from 'react-calendar';
// somewhere in src (e.g. main.tsx or App.tsx)
import 'react-calendar/dist/Calendar.css';
import { format } from 'date-fns';
import { useState } from 'react';


type DateSelectorProps = {
    date: Date;
    setDate: (d: Date) => void;
}
export default function DateSelector({date, setDate}: DateSelectorProps) {

    const [showCalendar, setShowCalendar] = useState(false);

    function addDate() {
        const newDate = addDays(date, 1);
        setDate(newDate);
    }

    function subDate() {
        const newDate = subDays(date, 1);
        setDate(newDate);
    }       

    return (
    <div>
        <div
            className="inline-flex rounded-md shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-primary-600 hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:bg-primary-600 focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] focus:outline-none focus:ring-0 active:bg-primary-700 active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.3),0_4px_18px_0_rgba(59,113,202,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(59,113,202,0.5)] dark:hover:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:focus:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)] dark:active:shadow-[0_8px_9px_-4px_rgba(59,113,202,0.2),0_4px_18px_0_rgba(59,113,202,0.1)]"
            role="group"
        >
            <button
                type="button"
                className="inline-block rounded-l bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white transition duration-150 ease-in-out hover:bg-primary-600 focus:bg-primary-600 focus:outline-none focus:ring-0 active:bg-primary-700"
                onClick={subDate}
            >
                -1
            </button>

            <button
                type="button"
                className="inline-block bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white transition duration-150 ease-in-out hover:bg-primary-600 focus:bg-primary-600 focus:outline-none focus:ring-0 active:bg-primary-700"
                onClick={() => setShowCalendar(!showCalendar)}
            >
            {format(date, 'yyyy-MM-dd')}
            </button>

            <button
                type="button"
                className="inline-block rounded-r bg-primary px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white transition duration-150 ease-in-out hover:bg-primary-600 focus:bg-primary-600 focus:outline-none focus:ring-0 active:bg-primary-700"
                onClick={addDate}
            >
                +1
            </button>

        </div>
        {showCalendar && <Calendar 
            onChange={(d) => setDate(d as Date)}/>}
    </div>
    );
}

