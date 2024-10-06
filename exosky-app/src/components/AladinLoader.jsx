import React, { useEffect, useRef, useState } from 'react';
import CoordsButton from './getCoords'; // Adjust the path if needed

const AladinLoader = () => {
    const aladinRef = useRef(null); // Reference to the Aladin Lite div
    const [aladinInstance, setAladinInstance] = useState(null); // Track the Aladin instance


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
            }
        };

        // Start the initialization process
        initializeAladin();

    },[]); // Only run once on mount


    return (
        <div>
            <div id="aladin-lite-div" ref={aladinRef} style={{ width: '100vw', height: '100vh' }}></div>
            <CoordsButton aladin={window.aladin} />
        </div>
    );
}

export default AladinLoader;
