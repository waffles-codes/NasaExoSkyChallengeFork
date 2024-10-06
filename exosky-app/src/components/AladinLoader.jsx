import React, { useEffect, useRef } from 'react';
import CoordsButton from './getCoords';

const AladinLoader = () => {
    const aladinRef = useRef(null); // Reference to the Aladin Lite div

    useEffect(() => {
        const initializeAladin = () => {
            if (window.A) {
                // Initialize Aladin viewer
                window.aladin = window.A.aladin(aladinRef.current, {
                    survey: "P/DSS2/color",
                    fov: 60,
                    target: 'andromeda galaxy'
                });
            }
        };

        // Start the initialization process
        initializeAladin();
    }, []); // Only run once on mount

    return (
        <div>
            <div id="aladin-lite-div" ref={aladinRef} style={{ width: '100vw', height: '100vh' }}></div>
            <CoordsButton aladin={window.aladin} />
        </div>
    );
}

export default AladinLoader;
