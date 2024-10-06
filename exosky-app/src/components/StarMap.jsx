import React, { useState, useEffect } from 'react';

function StarMap() {
  const [coords, setCoords] = useState([]);
  const [ra, setRa] = useState(0);
  const [dec, setDec] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCoords = () => {
    setIsLoading(true);
    setError(null);
    fetch(`http://localhost:5000/api/get_coords?inp_ra=${ra}&inp_dec=${dec}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setCoords(data);
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Error fetching coordinates:', error);
        setError(error.message);
        setIsLoading(false);
      });
  };

  useEffect(() => {
    fetchCoords();
  }, []); // Fetch initial data on component mount

  return (
    <div>
      <h1>Projected Star Coordinates</h1>
      <div>
        <label>
          RA:
          <input
            type="number"
            value={ra}
            onChange={(e) => setRa(parseFloat(e.target.value))}
          />
        </label>
        <label>
          Dec:
          <input
            type="number"
            value={dec}
            onChange={(e) => setDec(parseFloat(e.target.value))}
          />
        </label>
        <button onClick={fetchCoords}>Fetch Coordinates</button>
      </div>
      {isLoading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      <svg width="500" height="500" viewBox="-10 -10 20 20">
        {coords.map((coord, index) => (
          <circle
            key={index}
            cx={coord.x}
            cy={coord.y}
            r="0.1"
            fill="white"
          />
        ))}
      </svg>
    </div>
  );
}

export default StarMap;