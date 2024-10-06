import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import StarMap from '../components/StarMap.jsx';

const ExoSkyPage = () => {
    const navigate = useNavigate();
    const location = useLocation();

    // Extract RA/Dec values from location.state
    var { ra, dec } = location.state || { ra: 0, dec: 0 };

    const handleBackClick = () => {
        navigate('/', { state: { ra, dec } });
    };

    return (
        <div className='container'>
            <h1>Exosky Page</h1>

            {/* Back button */}
            <button onClick={handleBackClick} style={{ position: 'fixed', top: '0vh', left: '15vw' }}>
                Back
            </button>
            <StarMap/>
        </div>
    );
};

export default ExoSkyPage;
