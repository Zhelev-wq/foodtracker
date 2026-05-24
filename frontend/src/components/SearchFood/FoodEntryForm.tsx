import type { components } from '../../types/api.ts';
import { useState } from 'react'
import { api } from '../../api/client.ts'

type FoodEntryFormProps = {
    foodEntryFormData: null|components["schemas"]["FoodOut"],
    date: Date,
    isVisible: boolean,
    setVisible: (arg: boolean) => void
}

export default function FoodEntryForm({foodEntryFormData, date, isVisible, setVisible}: FoodEntryFormProps) {


    if (!isVisible || !foodEntryFormData) {
        return null;
    }
    
    function ProcessData(data: object){
        if (!data) {
            return <p>No data</p>
        }

        const details = Object.entries(data).map(
            (pair) => 
                <li>{pair[0]}: {pair[1] * ratio || 0}</li>
        )
        return details;
    }


    const {name, vitamins, minerals, fats, id, barcode, ...macros} = foodEntryFormData;
    

    const [grams, setGrams] = useState(100);
    const ratio = grams / 100;

    const macrosDetails = ProcessData(macros);
    const vitaminDetails = ProcessData(vitamins);
    const mineralDetails = ProcessData(minerals);
    const fatDetails = ProcessData(fats);

    return (
        <div className='border'>
            
            <div className="flex items-center">
                <h2>{name}</h2>
                <button
                    onClick={() => setVisible(false)}
                    >X</button>
            </div>
            

            <form>
                <div className="flex">
                    <input 
                    onChange={(e) => setGrams(Number(e.target.value))}
                    placeholder="weight" 
                    className="block w-full p-3 ps-9 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand shadow-xs placeholder:text-body" 
                    required/>

                    <button onClick={() => 
                        {
                            api.post('/api/create_food_entry',
                               {
                                food_uuid: id,
                                grams: grams
                                }
                            )
                        }
                        }>Add Entry</button>
                </div>
                <h3>Macros</h3>
                <ul className="col2">
                    {macrosDetails}
                </ul>
                <br></br>

                <h3>Vitamins</h3>
                <ul>
                    {vitaminDetails}
                </ul>
                                <br></br>

                <h3>Minerals</h3>
                <ul>
                    {mineralDetails}
                </ul>

                    <br></br>
                
                <h3>Fats</h3>
                <ul>
                    {fatDetails}
                </ul>
            </form>
        </div>
    )
}