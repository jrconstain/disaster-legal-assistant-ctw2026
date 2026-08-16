const { Groq } = require('groq-sdk');
const client = new Groq({ apiKey: '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' });
client.chat.completions.create({
    messages: [{role: 'user', content: 'hello'}],
    model: 'llama-3.1-8b-instant'
}).then(c => console.log("Success:", c.choices[0].message.content)).catch(e => console.error("Error:", e.message));
