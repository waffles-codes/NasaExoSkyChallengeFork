import React, { useEffect, useRef } from 'react';

const AladinViewer = () => {
    const aladinRef = useRef(null); // Reference to the Aladin Lite div

    useEffect(() => {
        const initializeAladin = () => {
            if (window.A) {
                // Initialize Aladin viewer
                window.A.aladin(aladinRef.current, { survey: "P/DSS2/color", fov: 60, target: 'andromeda galaxy' });
            } else {
                // If A is not ready, retry after 500 ms
                console.log("Waiting for Aladin script to load...");
                setTimeout(initializeAladin, 500);
            }
        };

        // Start the initialization process
        initializeAladin();

        // Capture the current value of aladinRef
        const currentRef = aladinRef.current;

        // Cleanup on unmount
        return () => {
            if (currentRef) {
                currentRef.innerHTML = ''; // Clear the div on unmount
            }
        };
    }, []); // Only run once on mount


    return (
        <div>
            <div id="aladin-lite-div" ref={aladinRef} style={{ width: '100vw', height: '100vh' }}></div>
        </div>
    );
}

export default AladinViewer;
