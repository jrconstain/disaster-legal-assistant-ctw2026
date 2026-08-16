const { Groq } = require('groq-sdk');
const client = new Groq({ apiKey: 'dummy', baseURL: 'http://localhost:11434/v1' });
client.chat.completions.create({
    messages: [{role: 'user', content: 'hello'}],
    model: 'qwen2.5:1.5b'
}).then(c => console.log("Success:", c.choices[0].message.content)).catch(e => console.error("Error:", e.message));
