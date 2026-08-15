const express = require('express');
const authRoutes = require('./features/auth/auth.routes');

const app = express();

// Middlewares
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/', authRoutes);

module.exports = app;
