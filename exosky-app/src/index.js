import React from 'react';
import ReactDOM from 'react-dom/client'; // Note: use 'react-dom/client' in React 18+
import App from './App'; // Import the main App component
import './styles.css';

// Create the root element
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
