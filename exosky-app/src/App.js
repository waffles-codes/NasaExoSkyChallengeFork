import React, { useEffect, useRef, useState } from 'react';

const AladinViewer = () => {
    var [target, setTarget] = useState('andromeda galaxy'); // Default
    const aladinRef = useRef(null); // Reference to the Aladin Lite div
    const [ra, setRa] = useState(''); // State to store RA
    const [dec, setDec] = useState(''); // State to store Dec

    // Function to resolve target name using Sesame
    const resolveSesame = (target) => {
        return new Promise((resolve, reject) => {
            if (window.Sesame) {
                window.Sesame.getTargetRADec(target,
                    function(data) {
                        setRa(data.ra.toPrecision(7)); // Set RA
                        setDec(data.dec.toPrecision(7)); // Set Dec
                        resolve(data);
                    },
                    function() {
                        reject('Could not resolve target');
                    }
                );
            } else {
                reject('Sesame library not loaded');
            }
        });
    };

    // Initialize Aladin viewer when submitting the target
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Construct the Sesame API URL
        const sesameUrl = `https://cds.unistra.fr/cgi-bin/nph-sesame/-oxp/${target}`;

        try {
            const response = await fetch(sesameUrl);

            // Check if the response is ok (status in the range 200-299)
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Parse the XML response
            const xmlText = await response.text();
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, "text/xml");

            // Extract relevant information
            const name = xmlDoc.getElementsByTagName("name")[0]?.textContent;
            const jpos = xmlDoc.getElementsByTagName("jpos")[0]?.textContent;

            if (name && jpos) {
                // Update the Aladin viewer with the resolved target
                if (window.aladin) {
                    window.aladin.setTarget(jpos);
                }
                console.log(`Resolved target: ${name}, Position: ${jpos}`);
            } else {
                console.error("No valid response received");
            }

        } catch (error) {
            console.error("Error fetching target data:", error);
        }

        // Initialize Aladin viewer if it hasn't been done yet
        if (!window.aladin && window.A) {
            window.aladin = window.A.aladin(aladinRef.current, {survey: "P/DSS2/color", fov: 60, target: target});
        }
    };


    const handleInputChange = (e) => {
        setTarget(e.target.value);
    };

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (window.aladin) {
                window.aladin = null; // Clear the global reference
            }
        };
    }, []); // Empty dependency array to run on unmount only

    return (
        <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
            <form onSubmit={handleSubmit} style={{ position: 'absolute', top: '20px', left: '20px'}}>
                <input
                    type="text"
                    value={target}
                    onChange={handleInputChange}
                    placeholder="Enter a celestial target"
                    style={{ padding: '8px', width: '300px' }} // Optional styling
                />
                <button type="submit">Go to Target</button>
            </form>
            <div ref={aladinRef} style={{ width: '100%', height: '100%' }}></div>
        </div>
    );
}

export default AladinViewer;