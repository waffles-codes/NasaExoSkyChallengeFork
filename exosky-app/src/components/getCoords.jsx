import React from 'react';
import { useNavigate } from 'react-router-dom';

const CoordsButton = ({ aladin }) => {
    const navigate = useNavigate()
    var [raValue, decValue] = ["",""];

    const onClick = () => {
        if (aladin) {
            [raValue, decValue] = aladin.getRaDec();
            console.log("RA:", raValue);
            console.log("Dec:", decValue);

        } else {
            console.log("Aladin instance is not available.");
        }

        // After fetching coords, navigate to the ExoSky page and pass ra and dec to API and to store location.
        navigate('/exosky', { state: { ra: raValue, dec: decValue } });
    };

    return (
        <div style={{ position: 'fixed', top: '4vh', left: '15vw' }}>
            <button onClick={onClick}>Get Exosky</button>
        </div>
    );
};

export default CoordsButton;
