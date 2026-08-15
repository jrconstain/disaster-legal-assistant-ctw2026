const express = require('express');
const authController = require('./auth.controller');

const router = express.Router();

router.get('/', authController.getIndexPage);
router.get('/api/status', authController.getStatus);

module.exports = router;
