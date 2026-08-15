const dbService = require('./db.service');
const welcomeFlow = require('./flows/welcome.flow');
const profilingFlow = require('./flows/profiling.flow');

const handleIncomingMessage = async (phoneNumber, messageText) => {
    try {
        const userState = dbService.getUserState(phoneNumber);

        // Si no ha dado su consentimiento (es null o false), lo maneja el flujo de bienvenida
        if (userState.consent !== true) {
            const welcomeResponse = welcomeFlow.handleWelcome(phoneNumber, messageText, userState);
            if (welcomeResponse) {
                return welcomeResponse;
            }
        }
        
        // Si ya dio el consentimiento (es true), lo maneja el flujo de perfilamiento (LLM)
        return await profilingFlow.handleProfiling(phoneNumber, messageText, userState);

    } catch (error) {
        console.error("Error procesando mensaje en chatbot:", error);
        return "Disculpa, tuvimos un problema técnico. Intenta nuevamente más tarde.";
    }
};

module.exports = {
    handleIncomingMessage
};
