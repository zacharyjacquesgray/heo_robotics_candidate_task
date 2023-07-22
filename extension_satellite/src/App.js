import React from "react";
import SatelliteOrbitMap from "./SatelliteOrbitMap";
import "./App.css";

const App = () => {
  return (
    <div>
      <SatelliteOrbitMap />
      <div className="header-container">
        <h1>SATELLITE TRACKER</h1>
        <h2>ZACHARY GRAY</h2>
      </div>
    </div>
  );
};

export default App;
