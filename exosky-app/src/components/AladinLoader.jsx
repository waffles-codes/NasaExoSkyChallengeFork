import React, { useEffect, useRef } from 'react';

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

    const onCoordsClick = () => {
        if (window.A && window.aladin) {
            var [raValue, decValue] = window.aladin.getRaDec();
            console.log("RA:", raValue);
            console.log("Dec:", decValue);
        }
    };

    return (
        <div>
            <div id="aladin-lite-div" ref={aladinRef} style={{ width: '100vw', height: '100vh' }}></div>
            <div id='coords' style={{ position: 'fixed', top: '4vh', left: '15vw' }}>
                <button id='coords-button' onClick={onCoordsClick}>Get coords</button>
            </div>
        </div>
    );
}

export default AladinLoader;
