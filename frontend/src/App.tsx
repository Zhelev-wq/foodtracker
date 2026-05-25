import axios from 'axios';
import { useState, useEffect } from 'react'
import './App.css'
import './components/DateSelector.js'
import DateSelector from './components/DateSelector.js'
import FoodItemList from './components/FoodItemList.js';
import FoodSummary from './components/FoodSummary.js'
import FoodSearchBar from './components/SearchFood/FoodSearchBar.js'
import FoodResultList from './components/SearchFood/FoodResultsList.js';
import { api } from './api/client';
import { format } from 'date-fns';

function App() {
  function getDate() {
        const timestamp = Date.now();
        const date = new Date(timestamp);
        return date;
  }

  const fetchFoodData = async () => {
    const response = await api.get(`/api/search/date/${format(date, 'yyyy-MM-dd')}`);
    setFoodData(response.data);
  };

  const [date, setDate] = useState(getDate());
  const [foodData, setFoodData] = useState([]);
  useEffect(() => {  
    fetchFoodData();
  }, [date]);

  const [searchText, setSearchText] = useState('');
  const [foodSearchResults, setFoodSearchResults] = useState(null);
  const [showFoodResultsSection, setShowFoodResultsSection] = useState(false);

  useEffect(() => {
    if (!searchText) {
      setFoodSearchResults(null);
      return
    };
    const t = setTimeout(() => {
      const fetchResults = async () => {
        const response = await api.get(`/api/search/name/${searchText}`)
        setFoodSearchResults(response.data);
        return response.data;
      }      
      fetchResults();
    }, 500);
    return () => clearTimeout(t);
  }, [searchText]);

  return (
    <>
      <section id="date-selector-location">      
        <DateSelector date={date} setDate={setDate}/>
      </section>
      <br></br>

      <section>
        <FoodSummary foodData={foodData} />
      </section>
      <br></br>

      <section>
        <div>
          <button 
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
            onClick={()=> setShowFoodResultsSection(!showFoodResultsSection)}>Add Food</button>
        </div>
      </section>
      <br></br>

      <section>
        <FoodItemList foodData={foodData} fetchFoodData={fetchFoodData}/>
      </section>
      <br></br>

      {showFoodResultsSection && 
        <section>
          <FoodSearchBar setSearchText={setSearchText} /> 
          <br></br>
          <FoodResultList foodSearchResults={foodSearchResults} date={date} /> 
      </section>}
      
    </>
  )
}

export default App
