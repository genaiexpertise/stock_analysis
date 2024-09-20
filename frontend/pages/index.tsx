"use client";

import Header from "@/components/Header";

import {useState} from "react";
import InputSection from "@/components/InputSection";

export default function Home() {
  const [company_stock, setCompanyStock] = useState([]);

  return (
    <div className="bg-white min-h-screen text-black">
      <Header />
      <div className="flex flex-col">
        <div className="flex w-full">
          <div className="w-1/2 p-4">
         
            <InputSection
              title="Company Stock"
              placeholder="Example: AAPL"
              data={company_stock}
              setData={setCompanyStock}
            />
          </div>
          
        </div>

        <div className="flex flex-col w-full p-4">
          {/* Output section and event log in a single column below */}
          <div className="flex justify-between items-center mb-4">
          <button
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded text-sm"
            >
              Start
           </button>


          {/* TODO: FINAL OUTPUT */}
          {/* TODO: EVENT LOG */}

          </div>
        </div>
      </div>
    </div>
  );
}