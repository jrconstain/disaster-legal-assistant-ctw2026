require('dotenv').config();
const app = require('./app');
const waClient = require('./globals/whatsapp');
const chatbotController = require('./features/chatbot/chatbot.controller');

const PORT = process.env.PORT || 3000;

const startServer = () => {
    app.listen(PORT, () => {
        console.log(`🚀 Server is running on http://localhost:${PORT}`);
    });
};

const initializeApp = () => {
    // Start Express server
    startServer();

    // Setup Chatbot listener
    waClient.client.on('message', async (msg) => {
        try {
            // Ignorar estados
            if (msg.from === 'status@broadcast') return;
            
            const isGroup = msg.from.endsWith('@g.us');
            const chatName = isGroup ? 'Grupo' : 'Privado';
            
            console.log(`[LOG] Mensaje de: ${chatName} | ID: ${msg.from} | Texto: ${msg.body}`);

            // Validar Whitelist
            const whitelistEnv = process.env.WHITELIST || '';
            const whitelist = whitelistEnv.split(',').map(id => id.trim()).filter(id => id);

            // Si no está en la whitelist, ignoramos el mensaje
            if (!whitelist.includes(msg.from)) {
                console.log(`[DEBUG] Ignorado por Whitelist. ID ${msg.from} no está en:`, whitelist);
                return;
            }
            
            // Procesamiento de audio
            let messageText = msg.body;
            if (msg.hasMedia) {
                const media = await msg.downloadMedia();
                if (media && media.mimetype.includes('audio')) {
                    console.log(`[DEBUG] Audio detectado, transcribiendo...`);
                    const groqProvider = require('./services/providers/groq.provider');
                    const transcribedText = await groqProvider.transcribeAudio(media.data, media.mimetype);
                    messageText = `[Nota de voz transcrita]: ${transcribedText}`;
                }
            }

            // Identificar el usuario real (en grupos es msg.author, en privados es msg.from)
            const userId = isGroup && msg.author ? msg.author : msg.from;
            
            console.log(`[DEBUG] Enviando a Chatbot: ${messageText} (Usuario: ${userId})`);
            const reply = await chatbotController.handleIncomingMessage(userId, messageText);
            console.log(`[DEBUG] Respuesta del Chatbot: ${reply}`);
            if (reply) {
                msg.reply(reply);
            }
        } catch (error) {
            console.error("Error al procesar el mensaje:", error);
        }
    });

    // Initialize WhatsApp Web Client
    waClient.initialize();
};

initializeApp();
