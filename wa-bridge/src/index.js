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

const ragService = require('./services/rag.service');

const initializeApp = async () => {
    // Start Express server
    startServer();

    // Initialize RAG Knowledge Base
    await ragService.init();

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
                try {
                    const media = await msg.downloadMedia();
                    if (media && media.mimetype.includes('audio')) {
                        console.log(`[DEBUG] Audio detectado, transcribiendo...`);
                        const groqProvider = require('./services/providers/groq.provider');
                        const transcribedText = await groqProvider.transcribeAudio(media.data, media.mimetype);
                        messageText = `[Nota de voz transcrita]: ${transcribedText}`;
                    }
                } catch (mediaError) {
                    console.error(`[ERROR] Falló la descarga o transcripción del audio: ${mediaError.message || mediaError}`);
                    msg.reply("Disculpa, tuve un problema procesando tu nota de voz (posible error de conexión con WhatsApp). ¿Podrías intentar escribiendo tu mensaje?");
                    return; // Abortamos el procesamiento de este mensaje
                }
            }

            // Identificar el usuario real (en grupos es msg.author, en privados es msg.from)
            const userId = isGroup && msg.author ? msg.author : msg.from;
            
            if (!global.messageQueues) {
                global.messageQueues = {};
            }

            if (!global.messageQueues[userId]) {
                global.messageQueues[userId] = {
                    messages: [],
                    timer: null,
                    lastMsg: null
                };
            }

            // Si el mensaje es una imagen sin texto, agregamos una nota
            const textToQueue = messageText ? messageText : (msg.hasMedia ? "[Imagen/Archivo adjunto]" : "");
            
            if (textToQueue.trim()) {
                global.messageQueues[userId].messages.push(textToQueue);
            }
            global.messageQueues[userId].lastMsg = msg;

            if (global.messageQueues[userId].timer) {
                clearTimeout(global.messageQueues[userId].timer);
            }

            global.messageQueues[userId].timer = setTimeout(async () => {
                const queueData = global.messageQueues[userId];
                delete global.messageQueues[userId];

                const combinedText = queueData.messages.join('\n');
                const finalMsg = queueData.lastMsg;

                if (!combinedText) return;

                console.log(`[DEBUG] Enviando a Chatbot (Agrupado): ${combinedText} (Usuario: ${userId})`);
                try {
                    const reply = await chatbotController.handleIncomingMessage(userId, combinedText);
                    console.log(`[DEBUG] Respuesta del Chatbot: ${reply}`);
                    if (reply) {
                        finalMsg.reply(reply);
                    }
                } catch (error) {
                    console.error("Error en procesamiento agrupado:", error);
                }
            }, 5000); // 5 segundos de espera
        } catch (error) {
            console.error("Error al procesar el mensaje:", error);
        }
    });

    // Initialize WhatsApp Web Client
    waClient.initialize();
};

initializeApp();
