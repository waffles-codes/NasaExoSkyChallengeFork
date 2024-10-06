import React from 'react';

const CoordsButton = ({ aladin }) => {
    const onClick = () => {
        if (aladin) {
            const [raValue, decValue] = aladin.getRaDec();
            console.log("RA:", raValue);
            console.log("Dec:", decValue);
            // Add any additional functionalities here
        } else {
            console.log("Aladin instance is not available.");
        }
    };

    return (
        <div style={{ position: 'fixed', top: '4vh', left: '15vw' }}>
            <button onClick={onClick}>Get Exosky</button>
        </div>
    );
};

export default CoordsButton;
