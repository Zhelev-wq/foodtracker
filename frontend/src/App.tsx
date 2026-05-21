import { useState, useEffect } from 'react'
import './App.css'
import './components/DateSelector.js'
import DateSelector from './components/DateSelector.js'
import FoodItemList from './components/FoodItemList.js';
import FoodSummary from './components/FoodSummary.js'
import axios from 'axios';

function App() {
  function getDate() {
        const timestamp = Date.now();
        const date = new Date(timestamp);
        return date;
  }

  const [date, setDate] = useState(getDate());
  const [foodData, setFoodData] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
        const isoDate = date.toISOString();
        const response = await axios.get(`http://127.0.0.1:8000/api/search/date/${isoDate}`);
        setFoodData(response.data);
    };

    fetchData();
  }, [date]);

  return (
    <>
      <section id="date-selector-location">      
        <DateSelector date={date} setDate={setDate}/>
      </section>

      <section>
        <FoodSummary foodData={foodData} />
      </section>

      <section>
        <FoodItemList foodData={foodData}/>
      </section>
    </>
  )
}

export default App
