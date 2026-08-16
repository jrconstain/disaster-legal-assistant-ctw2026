const groqProvider = require('./providers/groq.provider');
const ragService = require('./rag.service');
// const geminiProvider = require('./providers/gemini.provider'); // Para futuro

class LlmService {
    async processUserInteraction(systemPrompt, history, newMessage) {
        // 1. Consultar la Base de Conocimientos (RAG)
        const ragResults = ragService.searchKnowledge(newMessage);
        let finalSystemPrompt = systemPrompt;

        if (ragResults && ragResults.length > 0) {
            const contextText = ragResults.map((r, i) => `[Documento ${r.source} - Párrafo ${i+1}]:\n${r.content}`).join('\n\n');
            
            finalSystemPrompt += `\n\n=== CONTEXTO DE BASE DE CONOCIMIENTOS (RAG) ===\nEl usuario acaba de decir algo que coincide con nuestros manuales. Usa la siguiente información oficial para complementar tu respuesta de forma empática y clara. Si la información no es relevante para la pregunta exacta, ignórala y sigue tu flujo normal.\n\n${contextText}\n===============================================\n`;
            console.log(`[RAG] Contexto inyectado al prompt (${ragResults.length} párrafos encontrados).`);
        }

        const provider = process.env.LLM_PROVIDER || 'groq';

        switch (provider.toLowerCase()) {
            case 'groq':
                return await groqProvider.processMessage(finalSystemPrompt, history, newMessage);
            // case 'gemini':
            //     return await geminiProvider.processMessage(finalSystemPrompt, history, newMessage);
            default:
                console.warn(`Proveedor LLM no reconocido: ${provider}. Usando Groq por defecto.`);
                return await groqProvider.processMessage(finalSystemPrompt, history, newMessage);
        }
    }
}

module.exports = new LlmService();
