import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const ExoSkyPage = () => {
    const navigate = useNavigate();
    const location = useLocation();

    // Extract RA/Dec values from location.state
    var { ra, dec } = location.state || { ra: 0, dec: 0 };

    const handleBackClick = () => {
        navigate('/', { state: { ra, dec } });
    };

    return (
        <div>
            <h1>Exosky Page</h1>

            {/* Back button */}
            <button onClick={handleBackClick} style={{ position: 'fixed', top: '4vh', left: '15vw' }}>
                Back
            </button>
        </div>
    );
};

export default ExoSkyPage;
