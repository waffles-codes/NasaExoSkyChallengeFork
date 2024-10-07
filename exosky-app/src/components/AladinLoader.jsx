import React, { useEffect, useRef, useState } from 'react';
import CoordsButton from './getCoords';
import { useLocation } from 'react-router-dom';

const AladinLoader = () => {
    const aladinRef = useRef(null); // Reference to the Aladin Lite div
    const [aladinInstance, setAladinInstance] = useState(null); // Track the Aladin instance, kind of like an API key.
                                                                // needed to avoid prop reference breaking when sending to
                                                                // getCoords.
    const location = useLocation();

    useEffect(() => {
        const initializeAladin = () => {
            if (window.A) {
                // Initialize Aladin viewer and store the instance
                window.aladin = window.A.aladin(aladinRef.current, {
                    survey: "P/DSS2/color",
                    fov: 50,
                    target: 'andromeda galaxy'
                });
                setAladinInstance(window.aladin);

                // If RA/Dec values are passed, go to those coordinates
                if (location.state && location.state.ra && location.state.dec) {
                    window.aladin.gotoRaDec(location.state.ra, location.state.dec);
                }
            }
        };

        // Start the initialization process
        initializeAladin();

    }, [location.state]); // Re-run if location.state changes

    // Function to generate random celestial coordinates
    const generateRandomCoords = () => {
        const randomRA = (Math.random() * 360).toFixed(4);  // RA between 0.0000 and 360.0000
        const randomDec = (Math.random() * 180 - 90).toFixed(4);  // Dec between -90.0000 and 90.0000
        console.log("Random RA:", randomRA, "Random Dec:", randomDec);

        // Move Aladin to the random coordinates
        if (aladinInstance) {
            aladinInstance.gotoRaDec(randomRA, randomDec);
        }
    };


    return (
        <div>
            <div id="aladin-lite-div" ref={aladinRef} style={{ width: '100vw', height: '100vh' }}></div>
            <div style={{ position: 'fixed', top: '30px', left: '120px' }}>
                <CoordsButton aladin={window.aladin} />
                <button onClick={generateRandomCoords} style={{ marginLeft: '10px' }}>Random Coords</button>
            </div>
        </div>
    );
}

export default AladinLoader;
