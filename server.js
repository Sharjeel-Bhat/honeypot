const express = require('express');
const fs = require('fs');
const path = require('path');
const useragent = require('express-useragent');
const app = express();
const PORT = 3000;

// Middleware to parse user-agent
app.use(useragent.express());

// Middleware to log visitor details
app.use((req, res, next) => {
    const logEntry = `${new Date().toISOString()} - IP: ${req.ip} - Device: ${req.useragent.platform} - Browser: ${req.useragent.browser}\n`;
    fs.appendFileSync(path.join(__dirname, 'honeypot.log'), logEntry);
    next();
});

// Simulate a vulnerable endpoint
app.get('/admin', (req, res) => {
    res.status(403).send('Forbidden: You are not authorized to access this page.');
});

// Simulate fake sensitive data
app.get('/config', (req, res) => {
    res.status(200).send('DB_PASSWORD=supersecretpassword');
});

// Serve the frontend
app.use(express.static(path.join(__dirname)));

// Start the server
app.listen(PORT, () => {
    console.log(`Honeypot server running on http://localhost:${PORT}`);
});
