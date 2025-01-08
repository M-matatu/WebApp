import React, { useState, useEffect } from "react";
import axios from "axios";

// Utility function to generate a random 5-letter string
const generateRandomRouteId = () => {
  const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
  let routeId = "";
  for (let i = 0; i < 5; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    routeId += characters[randomIndex];
  }
  return routeId;
};

const FareRateManagementPage = () => {
  const [routes, setRoutes] = useState([]);
  const [newFareRate, setNewFareRate] = useState({
    fareRate: "",
    effectiveDate: "",
  });
  const [isModalOpen, setIsModalOpen] = useState(false); // For Modify modal
  const [isAddModalOpen, setIsAddModalOpen] = useState(false); // For Add New Entry modal
  const [newEntry, setNewEntry] = useState({
    route_start: "",
    route_end: "",
    fareRate: "",
    effectiveDate: "",
  });
  const [selectedRouteId, setSelectedRouteId] = useState(null); // This will store the routeId for modifying
  const [error, setError] = useState(""); // State for error message

  // Fetch data from the backend
  useEffect(() => {
    const fetchRoutes = async () => {
      try {
        const response = await axios.get("https://mmatatubackend.onrender.com/backend/fares/");
        const fetchedRoutes = response.data.fares.map((fare) => ({
          route_id: fare.route_id, 
          route_start: fare.route_start,
          route_end: fare.route_end,
          fareRate: fare.Rate,
          effectiveDate: fare.updated_at,
        }));
        setRoutes(fetchedRoutes);
      } catch (error) {
        setError("Error fetching routes. Please try again later.");
        console.error("Error fetching routes:", error);
      }
    };

    fetchRoutes();
  }, []);

  const handleFareRateChange = (e) => {
    const { name, value } = e.target;
    setNewFareRate({ ...newFareRate, [name]: value });
  };

  const handleNewEntryChange = (e) => {
    const { name, value } = e.target;
    setNewEntry({ ...newEntry, [name]: value });
  };

  // Handle updating fare rate
  const updateFareRate = async () => {
    try {
      await axios.put(`https://mmatatubackend.onrender.com/backend/fares/update/${selectedRouteId}/`, {
        Rate: newFareRate.fareRate,
        updated_at: newFareRate.effectiveDate,
      });

      setRoutes(
        routes.map((route) =>
          route.route_id === selectedRouteId
            ? { ...route, fareRate: newFareRate.fareRate, effectiveDate: newFareRate.effectiveDate }
            : route
        )
      );

      setIsModalOpen(false);
      setNewFareRate({ fareRate: "", effectiveDate: "" });
      setSelectedRouteId(null);
      setError(""); // Clear error after successful update
    } catch (error) {
      setError("Error updating fare rate. Please try again later.");
      console.error("Error updating fare rate:", error);
    }
  };

  const addNewEntry = async () => {
    try {
      const newRouteId = generateRandomRouteId(); // Generate a random route_id

      await axios.post("https://mmatatubackend.onrender.com/backend/fares/", {
        route_start: newEntry.route_start,
        route_end: newEntry.route_end,
        Rate: newEntry.fareRate,
        updated_at: newEntry.effectiveDate,
        route_id: newRouteId, // Add the generated route_id
      });

      setRoutes((prevRoutes) => [
        ...prevRoutes,
        {
          route_id: newRouteId,
          route_start: newEntry.route_start,
          route_end: newEntry.route_end,
          fareRate: newEntry.fareRate,
          effectiveDate: newEntry.effectiveDate,
        },
      ]);

      // Close modal and reset form
      setIsAddModalOpen(false);
      setNewEntry({ route_start: "", route_end: "", fareRate: "", effectiveDate: "" });
      setError(""); // Clear error after successful addition
    } catch (error) {
      setError("Error adding new entry. Please try again later.");
      console.error("Error adding new entry:", error);
    }
  };

  const openModal = (route) => {
    setSelectedRouteId(route.route_id);
    setNewFareRate({
      fareRate: route.fareRate,
      effectiveDate: route.effectiveDate,
    });
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setNewFareRate({ fareRate: "", effectiveDate: "" });
    setSelectedRouteId(null);
  };

  const openAddModal = () => {
    setIsAddModalOpen(true);
  };

  const closeAddModal = () => {
    setIsAddModalOpen(false);
    setNewEntry({ route_start: "", route_end: "", fareRate: "", effectiveDate: "" });
  };

  return (
    <div className="p-8 bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
      <h2 className="text-4xl font-bold text-center mb-8 text-shadow-md">
        Fare Rate Management
      </h2>

      {/* Error Message Display */}
      {error && (
        <div className="bg-red-600 text-white p-4 mb-4 rounded-md">
          {error}
        </div>
      )}

      {/* Fare Overview Section */}
      <div className="mb-8 flex justify-between">
        <h3 className="text-2xl font-semibold mb-4 text-blue-800">
          Current Fare Rates
        </h3>
        <button
          onClick={openAddModal}
          className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transform hover:scale-105 transition-all duration-300"
        >
          Add New Entry
        </button>
      </div>
      <table className="min-w-full table-auto bg-white text-gray-800">
        <thead>
          <tr className="bg-blue-800 text-white">
            <th className="px-6 py-3 text-left">Route Start</th>
            <th className="px-6 py-3 text-left">Route End</th>
            <th className="px-6 py-3 text-left">Current Fare Rate</th>
            <th className="px-6 py-3 text-left">Effective Date</th>
            <th className="px-6 py-3 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {routes.map((route) => (
            <tr
              key={route.route_id}
              className="border-b hover:bg-blue-100 transition-all duration-300"
            >
              <td className="px-6 py-4">{route.route_start}</td>
              <td className="px-6 py-4">{route.route_end}</td>
              <td className="px-6 py-4">
                Ksh{parseFloat(route.fareRate).toFixed(2)}
              </td>
              <td className="px-6 py-4">
                {new Date(route.effectiveDate).toLocaleString()}
              </td>
              <td className="px-6 py-4">
                <button
                  onClick={() => openModal(route)}
                  className="text-yellow-500 hover:text-yellow-700 transform hover:scale-110 transition-all duration-300"
                >
                  Modify
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Add New Entry Modal */}
      {isAddModalOpen && (
        <div className="fixed inset-0 flex justify-center items-center bg-gray-800 bg-opacity-50 z-50">
          <div className="bg-white p-8 rounded-lg shadow-lg max-w-lg w-full">
            <h3 className="text-2xl font-semibold mb-4 text-blue-800">
              Add New Fare Rate
            </h3>
            <form>
              <div className="mb-4">
                <label className="block mb-2 text-gray-800">Route Start</label>
                <input
                  type="text"
                  name="route_start"
                  value={newEntry.route_start}
                  onChange={handleNewEntryChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block mb-2 text-gray-800">Route End</label>
                <input
                  type="text"
                  name="route_end"
                  value={newEntry.route_end}
                  onChange={handleNewEntryChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block mb-2 text-gray-800">Fare Rate (Ksh)</label>
                <input
                  type="number"
                  name="fareRate"
                  value={newEntry.fareRate}
                  onChange={handleNewEntryChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block mb-2 text-gray-800">Effective Date</label>
                <input
                  type="date"
                  name="effectiveDate"
                  value={newEntry.effectiveDate}
                  onChange={handleNewEntryChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={closeAddModal}
                  className="px-6 py-2 bg-gray-500 text-white rounded-lg mr-4 hover:bg-gray-600"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={addNewEntry}
                  className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
                >
                  Add Entry
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modify Fare Rate Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 flex justify-center items-center bg-gray-800 bg-opacity-50 z-50">
          <div className="bg-white p-8 rounded-lg shadow-lg max-w-lg w-full">
            <h3 className="text-2xl font-semibold mb-4 text-blue-800">
              Modify Fare Rate
            </h3>
            <form>
              <div className="mb-4">
                <label className="block mb-2 text-gray-800">Fare Rate (Ksh)</label>
                <input
                  type="number"
                  name="fareRate"
                  value={newFareRate.fareRate}
                  onChange={handleFareRateChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block mb-2 text-gray-800">Effective Date</label>
                <input
                  type="date"
                  name="effectiveDate"
                  value={newFareRate.effectiveDate}
                  onChange={handleFareRateChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={closeModal}
                  className="px-6 py-2 bg-gray-500 text-white rounded-lg mr-4 hover:bg-gray-600"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={updateFareRate}
                  className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  Update Fare Rate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FareRateManagementPage;
