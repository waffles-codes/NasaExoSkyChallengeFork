import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import StarMap from '../components/StarMap.jsx';
import ExoSkyCanvas from "../components/ExoSkyCanvas";

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
            <button onClick={handleBackClick} style={{ position: 'fixed', top: '0vh', left: '15vw' }}>
                Back
            </button>
            <StarMap/>
            <ExoSkyCanvas/>
        </div>
    );
};

export default ExoSkyPage;