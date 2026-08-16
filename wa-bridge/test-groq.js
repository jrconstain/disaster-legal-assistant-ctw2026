require('dotenv').config();
console.log("Key:", process.env.GROQ_API_KEY ? "EXISTS" : "MISSING", process.env.GROQ_API_KEY?.substring(0,8));
const { Groq } = require('groq-sdk');
const client = new Groq({ apiKey: process.env.GROQ_API_KEY });
client.chat.completions.create({
    messages: [{role: 'user', content: 'hello'}],
    model: 'llama-3.1-8b-instant'
}).then(c => console.log("Success:", c.choices[0].message.content)).catch(e => console.error("Error:", e.message));
