const groqProvider = require('./providers/groq.provider');
// const geminiProvider = require('./providers/gemini.provider'); // Para futuro

class LlmService {
    async processUserInteraction(systemPrompt, history, newMessage) {
        const provider = process.env.LLM_PROVIDER || 'groq';

        switch (provider.toLowerCase()) {
            case 'groq':
                return await groqProvider.processMessage(systemPrompt, history, newMessage);
            // case 'gemini':
            //     return await geminiProvider.processMessage(systemPrompt, history, newMessage);
            default:
                console.warn(`Proveedor LLM no reconocido: ${provider}. Usando Groq por defecto.`);
                return await groqProvider.processMessage(systemPrompt, history, newMessage);
        }
    }
}

module.exports = new LlmService();
