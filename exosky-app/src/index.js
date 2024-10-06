import React from 'react';
import ReactDOM from 'react-dom/client'; // Ensure you have the latest version of React 18
import App from './App'; // Import the main App component
import { HashRouter as Router } from 'react-router-dom'; // Import BrowserRouter for routing
import './styles.css';

// Create a root element
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App wrapped with Router
root.render(
    <Router>
        <App />
    </Router>
);
