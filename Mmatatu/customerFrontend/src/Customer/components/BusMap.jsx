import { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

export default function BusMap() {
  const mapContainer = useRef(null);
  const map = useRef(null);

  useEffect(() => {
    if (map.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [36.8219, -1.2921],
      zoom: 12,
    });
  }, []);

  const sendDataToBackend = async () => {
    const data = { message: "Bus location data" }; 

    try {
      const response = await fetch("http://localhost:8000/mqtt/send/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();
      console.log("Data sent successfully:", result);
    } catch (error) {
      console.error("Error sending data:", error);
    }
  };

  return (
    <div className="relative w-full h-[calc(100vh-72px)] overflow-hidden">
      <div ref={mapContainer} className="absolute top-0 left-0 w-full h-full" />
      <button 
        onClick={sendDataToBackend} 
        className="absolute top-4 right-4 bg-blue-500 text-white px-4 py-2 rounded"
      >
        Send Data
      </button>
    </div>
  );
}