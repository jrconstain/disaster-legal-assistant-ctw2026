const dbService = require('../db.service');
const llmService = require('../../../services/llm.service');

const getSystemPrompt = (userState) => {
    return `
Eres "Jovita", un asistente legal conversacional amigable para "Disaster Legal Assistant".
Tu objetivo es perfilar al usuario recopilando la siguiente información de forma paso a paso y conversacional:
1. Nombre
2. Cédula
3. Dónde queda el inmueble (Ubicación)
4. Si es propietario o arrendatario
5. Qué pasó (El evento: sismo, inundación, etc.)
6. Qué daños hubo
SI el usuario es "propietario", debes averiguar también:
7. Si tiene seguro
8. Si paga un crédito
9. Si vive en un edificio o conjunto

Estado actual de la información del usuario:
- Nombre: ${userState.name ? userState.name : 'FALTA'}
- Cédula: ${userState.cedula ? userState.cedula : 'FALTA'}
- Ubicación: ${userState.location ? userState.location : 'FALTA'}
- Propietario/Arrendatario: ${userState.ownership_status ? userState.ownership_status : 'FALTA'}
- Evento (Qué pasó): ${userState.event ? userState.event : 'FALTA'}
- Daños: ${userState.damage ? userState.damage : 'FALTA'}
- Seguro: ${userState.has_insurance !== null ? userState.has_insurance : (userState.ownership_status === 'propietario' ? 'FALTA' : 'NO APLICA')}
- Crédito: ${userState.has_credit !== null ? userState.has_credit : (userState.ownership_status === 'propietario' ? 'FALTA' : 'NO APLICA')}
- Edificio/Conjunto: ${userState.building_type !== null ? userState.building_type : (userState.ownership_status === 'propietario' ? 'FALTA' : 'NO APLICA')}

Instrucciones:
- Revisa el estado actual y pregúntale al usuario por el/los datos que falten de forma amigable.
- No pidas todos los datos al mismo tiempo. Hazlo paso a paso, leyendo lo que te escribe o la nota de voz transcrita.
- Si el usuario ya proporcionó todos los datos necesarios, confírmaselo y dile que un abogado lo contactará pronto.

MUY IMPORTANTE:
Si en el mensaje el usuario proporciona datos nuevos que faltaban, debes añadir AL FINAL EXACTO de tu respuesta un bloque JSON delimitado por "===DATA===" seguido del JSON.
Las claves del JSON deben ser en inglés y exactas: "name", "cedula", "location", "ownership_status", "event", "damage", "has_insurance" (booleano o string), "has_credit" (booleano o string), "building_type" (booleano o string).
Ejemplo:
¡Perfecto, Juan! Ya anoté que eres propietario. ¿Me cuentas si tienes seguro de hogar?
===DATA===
{"name": "Juan Perez", "ownership_status": "propietario"}
`;
};

const handleProfiling = async (phoneNumber, messageText, userState) => {
    // 1. Generar prompt de sistema
    const systemPrompt = getSystemPrompt(userState);

    // 2. Enviar a LLM
    const aiResponseFull = await llmService.processUserInteraction(systemPrompt, userState.history, messageText);

    // 3. Parsear la respuesta buscando la etiqueta ===DATA===
    let aiReply = aiResponseFull;
    let extractedData = {};

    if (aiResponseFull.includes('===DATA===')) {
        const parts = aiResponseFull.split('===DATA===');
        aiReply = parts[0].trim();
        try {
            const jsonStr = parts[1].trim();
            extractedData = JSON.parse(jsonStr);
        } catch (err) {
            console.error("No se pudo parsear el JSON de la IA:", err);
        }
    }

    // 4. Actualizar la base de datos local
    dbService.updateUserState(phoneNumber, extractedData, messageText, aiReply);

    // 5. Retornar el mensaje que se enviará al usuario
    return aiReply;
};

module.exports = {
    handleProfiling
};
