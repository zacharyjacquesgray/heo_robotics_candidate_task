import React, { useEffect, useState } from 'react';
import { GoogleMap, Marker, Polyline } from "@react-google-maps/api";
import { twoline2satrec, propagate, degreesLat, degreesLong, eciToGeodetic, gstime } from 'satellite.js';


// Define the container style and map properties
const mapContainerStyle = {
    width: "100%",
    height: "100vh",
};

const mapOptions = {
    mapTypeId: 'satellite',
    zoom: 3,
};

const issIcon = {
    url: "./ISS_icon.png", // url of the image
    size: { width: 140, height: 110 }, // size of the image
    scaledSize: { width: 140, height: 110 }, // scaled size of the image
    anchor: { x: 70, y: 55 } // anchor point
  };

// Define a function to calculate the latitude and longitude of a point on an orbit
const getLatLng = (tleLine1, tleLine2, timeOffsetMinutes) => {
    // Parse TLE data and get the satellite object
    const satrec = twoline2satrec(tleLine1, tleLine2);

    // Get the current time in UTC (as a Date object)
    const currentTime = new Date();

    // Increment the time by the specified offset in minutes
    currentTime.setMinutes(currentTime.getMinutes() + timeOffsetMinutes);

    // Get the position and velocity of the satellite at the current time
    const positionAndVelocity = propagate(satrec, currentTime);

    // Get the geodetic position (latitude, longitude, altitude) of the satellite
    const geodeticCoordinates = eciToGeodetic(positionAndVelocity.position, gstime(currentTime));

    // Return the latitude and longitude in degrees
    return {
        lat: degreesLat(geodeticCoordinates.latitude),
        lng: degreesLong(geodeticCoordinates.longitude)
    };
};


// Define the main component that renders the map and the orbit path
const SatelliteOrbitMap = () => {
    const tleLine1 = "1 25544U 98067A   23201.85187593  .00013285  00000-0  24117-3 0  9991";
    const tleLine2 = "2 25544  51.6411 161.7191 0000450  86.8326   1.2108 15.49901597407012";

    // Calculate the orbit path using the getLatLng function
    const orbitPath = [];
    const timeStepMinutes = 1; // Time step in minutes, adjust as needed
    for (let i = -46; i < 46; i++) {
        let point = getLatLng(tleLine1, tleLine2, i * timeStepMinutes);
        orbitPath.push(point);
    }

    console.log(orbitPath)

    const [currentPosition, setCurrentPosition] = useState(null);

    useEffect(() => {
        // Function to update the currentPosition with the result of getLatLng(tleLine1, tleLine2, 0)
        const updatePosition = () => {
            const newPosition = getLatLng(tleLine1, tleLine2, 0);
            setCurrentPosition(newPosition);
        };

        // Update the currentPosition every second
        const interval = setInterval(updatePosition, 1000);

        // Fetch the initial position when the component mounts
        updatePosition();

        // Cleanup the interval on component unmount
        return () => clearInterval(interval);
    }, []);

    return (
        <GoogleMap
            mapContainerStyle={mapContainerStyle}
            center={currentPosition}
            zoom={mapOptions.zoom}
            mapTypeId={mapOptions.mapTypeId}
            apiKey="GOOGLE_API_KEY_HERE"
        >
            {currentPosition && <Polyline path={orbitPath} options={{ strokeColor: 'yellow' }} />}

            {currentPosition && <Marker position={currentPosition} icon={issIcon} />}
        </GoogleMap>
    );
};

export default SatelliteOrbitMap;