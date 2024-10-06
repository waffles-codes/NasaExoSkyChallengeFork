import React from 'react';
import { Route, Routes } from 'react-router-dom'; // Remove Router import
import AladinLoader from './components/AladinLoader';
import ExoSkyPage from './routes/ExoSkyPage';

const App = () => {
    return (
        <Routes>
            <Route path="/" element={<AladinLoader />} />
            <Route path="/exosky" element={<ExoSkyPage />} />
        </Routes>
    );
}

export default App;
