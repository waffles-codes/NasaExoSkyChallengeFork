import React, { useEffect, useRef, useState } from 'react';

const AladinViewer = () => {
    const [target, setTarget] = useState('Trifid nebula') //Default
    const aladinRef = useRef(null); // Reference to the Aladin Lite div

    useEffect(() => {
        const initializeAladin = () => {
            if (window.A) {
                // Initialize Aladin viewer
                window.A.aladin(aladinRef.current, { survey: "P/DSS2/color", fov: 60, target: target });
            } else {
                // If A is not ready, retry after 100 ms
                setTimeout(initializeAladin, 100);
            }
        };

        // Start the initialization process
        initializeAladin();

        // Cleanup on unmount
        return () => {
            if (aladinRef.current) {
                aladinRef.current.innerHTML = ''; // Clear the div on unmount
            }
        };
    }, [target]); // Re-run effect if target changes

    return (
        <div>
            <div id="aladin-lite-div" ref={aladinRef} style={{ width: '100vw', height: '100vh' }}></div>
        </div>
    );
}

export default AladinViewer;

