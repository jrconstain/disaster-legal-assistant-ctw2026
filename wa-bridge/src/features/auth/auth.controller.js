const waClient = require('../../globals/whatsapp');
const path = require('path');

const getIndexPage = (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'index.html'));
};

const getStatus = (req, res) => {
    res.json({
        status: waClient.getStatus(),
        qr: waClient.getQr()
    });
};

module.exports = {
    getIndexPage,
    getStatus
};
