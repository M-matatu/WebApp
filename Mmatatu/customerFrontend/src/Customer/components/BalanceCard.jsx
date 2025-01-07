import React, { useEffect, useState } from "react";

export default function BalanceCard({ username }) {
  const [balance, setBalance] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState("");
  const [amount, setAmount] = useState("");

  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const response = await fetch(`https://mmatatubackend.onrender.com/backend/api/balance?username=${username}`); // Fetch balance based on username
        const data = await response.json();
        setBalance(data.balance); // Assuming the response has a balance field
      } catch (error) {
        console.error("Error fetching balance:", error);
      }
    };

    if (username) {
      fetchBalance();
    }
  }, [username]);

  const handleRecharge = async () => {
    try {
        const username = localStorage.getItem("username"); // Get the username from local storage
        
        const response = await fetch("http://localhost:8000/pay/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
                phone_number: phoneNumber, 
                amount: amount, 
                username: username // Use the username from local storage
            }),
        });

        const result = await response.json();
        console.log("Recharge response:", result);
        setIsModalOpen(false); // Close the modal after the request
    } catch (error) {
        console.error("Error during recharge:", error);
    }
};

  return (
    <div className="bg-white p-4 rounded shadow-md">
      <h2 className="text-lg font-semibold">Balance</h2>
      <p className="text-2xl font-bold text-green-500">KSh {balance}</p>
      <button 
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
        onClick={() => setIsModalOpen(true)}
      >
        Recharge via M-Pesa
      </button>

      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded shadow-md">
            <h3 className="text-lg font-semibold">Recharge</h3>
            <div className="mt-4">
              <label className="block text-sm font-medium">Phone Number</label>
              <input 
                type="text" 
                value={phoneNumber} 
                onChange={(e) => setPhoneNumber(e.target.value)} 
                className="mt-1 p-2 border rounded w-full"
                required
              />
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium">Amount</label>
              <input 
                type="number" 
                value={amount} 
                onChange={(e) => setAmount(e.target.value)} 
                className="mt-1 p-2 border rounded w-full"
                required
              />
            </div>
            <div className="mt-4 flex justify-end">
              <button 
                className="mr-2 bg-gray-300 px-4 py-2 rounded" 
                onClick={() => setIsModalOpen(false)}
              >
                Cancel
              </button>
              <button 
                className="bg-blue-500 text-white px-4 py-2 rounded" 
                onClick={handleRecharge}
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}