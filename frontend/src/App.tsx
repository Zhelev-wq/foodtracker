import axios from 'axios';
import { useState, useEffect } from 'react'
import './App.css'
import './components/DateSelector.js'
import DateSelector from './components/DateSelector.js'
import FoodItemList from './components/FoodItemList.js';
import FoodSummary from './components/FoodSummary.js'
import AddFoodButton from './components/SearchFood/AddFoodButton.js'
import FoodSearchBar from './components/SearchFood/FoodSearchBar.js'
import FoodResultList from './components/SearchFood/FoodResultsList.js';
import { api } from './api/client';

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
        const response = await api.get(`/api/search/date/${isoDate}`);
        setFoodData(response.data);
    };

    fetchData();
  }, [date]);

  const [searchText, setSearchText] = useState('');
  const [foodSearchResults, setFoodSearchResults] = useState([]);
  useEffect(() => {
    if (!searchText) {
      setFoodSearchResults([]);
      return
    };
    const t = setTimeout(() => {
      console.log(searchText);
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
        <AddFoodButton />
      </section>
      <br></br>

      <section>
        <FoodItemList foodData={foodData}/>
      </section>
      <br></br>

      <section>
        <FoodSearchBar setSearchText={setSearchText} /> 
        <br></br>
        <FoodResultList foodSearchResults={foodSearchResults} date={date} /> 
      </section>
      
    </>
  )
}

export default App
