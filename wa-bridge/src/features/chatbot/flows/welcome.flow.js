const dbService = require('../db.service');

const handleWelcome = (phoneNumber, messageText, userState) => {
    if (userState.consent === null) {
        const isYes = /^(si|sí|✅ si|✅ sí|yes|acepto)/i.test(messageText.trim());
        const isNo = /^(no|❌ no|no acepto)/i.test(messageText.trim());
        
        if (isYes) {
            dbService.updateUserState(phoneNumber, { consent: true }, messageText, "Mensaje de bienvenida enviado");
            return `¡Excelente! 🙌 

Para empezar, *cuéntame tu caso como te salga*, por texto o nota de voz: dónde queda📍, si eres propietario o arrendatario 🏠, qué pasó y qué daños hubo 💥. Si eres propietario, dime también si tienes seguro, pagas un crédito o vives en un edificio o conjunto.

📎 Puedes enviarme fotos, videos o documentos. *Si no tienes todo claro, no te preocupes que yo te iré guiando.*`;

        } else if (isNo) {
            dbService.updateUserState(phoneNumber, { consent: false }, messageText, "Consentimiento denegado");
            return "Entendido. No podemos procesar tu solicitud ya que no autorizaste el tratamiento de datos. Si cambias de opinión, envíanos un 'Sí'.";
        } else {
            return `Hola 👋 Soy *Jovita, una IA*. Estoy aquí para ayudarte si tu inmueble sufrió daños por un sismo, inundación, deslizamiento u otra emergencia.

Puedo revisar contratos o pólizas, organizar tus evidencias y ayudarte a *preparar una reclamación o comunicación*. 📄

Para poder empezar a guiarte, voy a necesitar algunos datos personales y los documentos que compartas. Al continuar, autorizas su uso únicamente para analizar tu caso y preparar los documentos que solicites, de acuerdo con la *Ley 1581 de 2012*. Más información: *[link]*.

*¿Autorizas el tratamiento de tus datos para continuar?*

✅ Sí
❌ No`;
        }
    } else if (userState.consent === false) {
        const isYes = /^(si|sí|✅ si|✅ sí|yes|acepto)/i.test(messageText.trim());
        if (isYes) {
            dbService.updateUserState(phoneNumber, { consent: true }, messageText, "Consentimiento aceptado tras negación");
            return `¡Excelente! 🙌 

Para empezar, *cuéntame tu caso como te salga*, por texto o nota de voz: dónde queda📍, si eres propietario o arrendatario 🏠, qué pasó y qué daños hubo 💥. Si eres propietario, dime también si tienes seguro, pagas un crédito o vives en un edificio o conjunto.

📎 Puedes enviarme fotos, videos o documentos. *Si no tienes todo claro, no te preocupes que yo te iré guiando.*`;
        }
        return "No podemos procesar tu solicitud ya que previamente no autorizaste el tratamiento de datos. Si deseas autorizarlo ahora, responde 'Sí'.";
    }

    return null;
};

module.exports = {
    handleWelcome
};
