const { Groq } = require('groq-sdk');
const fs = require('fs');
const path = require('path');
const os = require('os');

class GroqProvider {
    constructor() {
        this.client = new Groq({
            apiKey: process.env.GROQ_API_KEY
        });
        // Usamos un modelo válido de Groq
        this.model = 'llama-3.3-70b-versatile';
    }

    async processMessage(systemPrompt, history, newMessage) {
        // Preparar mensajes
        const messages = [
            { role: 'system', content: systemPrompt },
            ...history,
            { role: 'user', content: newMessage }
        ];

        try {
            const completion = await this.client.chat.completions.create({
                messages: messages,
                model: this.model,
                temperature: 0.3, // Temperatura baja para que sea conciso y estructurado
            });

            return completion.choices[0]?.message?.content || "";
        } catch (error) {
            console.error("Error en Groq API:", error);
            // Si el modelo principal falla, intentar con un modelo por defecto de Groq como fallback.
            if (error.message && error.message.includes('model')) {
                console.warn(`Falló el modelo ${this.model}, intentando con llama3-8b-8192...`);
                try {
                    const fallbackCompletion = await this.client.chat.completions.create({
                        messages: messages,
                        model: 'llama3-8b-8192',
                        temperature: 0.3,
                    });
                    return fallbackCompletion.choices[0]?.message?.content || "";
                } catch(fallbackErr) {
                     console.error("Error en fallback de Groq API:", fallbackErr);
                     return "Lo siento, estoy teniendo problemas técnicos en este momento.";
                }
            }
            return "Lo siento, estoy teniendo problemas técnicos en este momento.";
        }
    }

    async transcribeAudio(base64Data, mimetype) {
        // Guardar archivo temporal
        const ext = mimetype.split('/')[1].split(';')[0]; // ej: ogg
        const tempFilePath = path.join(os.tmpdir(), `whatsapp_audio_${Date.now()}.${ext}`);
        
        try {
            fs.writeFileSync(tempFilePath, Buffer.from(base64Data, 'base64'));
            
            const transcription = await this.client.audio.transcriptions.create({
                file: fs.createReadStream(tempFilePath),
                model: 'whisper-large-v3',
                language: 'es'
            });

            return transcription.text;
        } catch (error) {
            console.error("Error transcribiendo audio con Groq:", error);
            return "[Error al transcribir el audio]";
        } finally {
            if (fs.existsSync(tempFilePath)) {
                fs.unlinkSync(tempFilePath);
            }
        }
    }
}

module.exports = new GroqProvider();
