const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode');

class WhatsAppClient {
    constructor() {
        this.client = new Client({
            authStrategy: new LocalAuth(),
            puppeteer: {
                executablePath: '/usr/bin/chromium',
                args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
                timeout: 60000,
                protocolTimeout: 300000
            }
        });

        this.qrCodeDataUrl = null;
        this.status = 'INITIALIZING';

        this._initializeEvents();
    }

    _initializeEvents() {
        this.client.on('qr', async (qr) => {
            console.log('QR RECEIVED');
            try {
                this.qrCodeDataUrl = await qrcode.toDataURL(qr);
                this.status = 'AWAITING_SCAN';
            } catch (err) {
                console.error('Error generating QR code data URL', err);
            }
        });

        this.client.on('ready', () => {
            console.log('Client is ready!');
            this.status = 'CONNECTED';
            this.qrCodeDataUrl = null;
        });

        this.client.on('authenticated', () => {
            console.log('AUTHENTICATED');
            this.status = 'AUTHENTICATED';
        });

        this.client.on('auth_failure', msg => {
            console.error('AUTHENTICATION FAILURE', msg);
            this.status = 'AUTH_FAILURE';
        });

        this.client.on('disconnected', (reason) => {
            console.log('Client was logged out', reason);
            this.status = 'DISCONNECTED';
            this.qrCodeDataUrl = null;
            
            // Reinitialize
            this.client.initialize();
        });
    }

    initialize() {
        console.log('Initializing WhatsApp Client...');
        this.client.initialize();
    }

    getQr() {
        return this.qrCodeDataUrl;
    }

    getStatus() {
        return this.status;
    }
}

const waClient = new WhatsAppClient();

module.exports = waClient;
