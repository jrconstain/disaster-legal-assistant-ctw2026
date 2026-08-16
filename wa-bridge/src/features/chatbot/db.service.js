const fs = require('fs');
const path = require('path');

const DB_PATH = path.join(__dirname, '../../data/users.json');

const readDB = () => {
    try {
        const data = fs.readFileSync(DB_PATH, 'utf8');
        return JSON.parse(data);
    } catch (err) {
        console.error('Error reading DB:', err);
        return {};
    }
};

const writeDB = (data) => {
    try {
        fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2), 'utf8');
    } catch (err) {
        console.error('Error writing DB:', err);
    }
};

const getUserState = (phoneNumber) => {
    const db = readDB();
    if (!db[phoneNumber]) {
        db[phoneNumber] = {
            phone: phoneNumber,
            name: null,
            cedula: null,
            claim: null,
            location: null,
            ownership_status: null,
            event: null,
            damage: null,
            has_insurance: null,
            has_credit: null,
            building_type: null,
            bank: null,
            policy_number: null,
            credit_balance: null,
            insured_value: null,
            expenses: null,
            radicado: null,
            stage: 'PROFILING',
            consent: null,
            is_confirmed: false,
            history: []
        };
        writeDB(db);
    }
    return db[phoneNumber];
};

const updateUserState = (phoneNumber, newData, newMessage, aiReply) => {
    const db = readDB();
    if (db[phoneNumber]) {
        // Actualizar campos extraídos
        if (newData.name !== undefined) db[phoneNumber].name = newData.name;
        if (newData.cedula !== undefined) db[phoneNumber].cedula = newData.cedula;
        if (newData.claim !== undefined) db[phoneNumber].claim = newData.claim;
        if (newData.location !== undefined) db[phoneNumber].location = newData.location;
        if (newData.ownership_status !== undefined) db[phoneNumber].ownership_status = newData.ownership_status;
        if (newData.event !== undefined) db[phoneNumber].event = newData.event;
        if (newData.damage !== undefined) db[phoneNumber].damage = newData.damage;
        if (newData.has_insurance !== undefined) db[phoneNumber].has_insurance = newData.has_insurance;
        if (newData.has_credit !== undefined) db[phoneNumber].has_credit = newData.has_credit;
        if (newData.building_type !== undefined) db[phoneNumber].building_type = newData.building_type;
        if (newData.bank !== undefined) db[phoneNumber].bank = newData.bank;
        if (newData.policy_number !== undefined) db[phoneNumber].policy_number = newData.policy_number;
        if (newData.credit_balance !== undefined) db[phoneNumber].credit_balance = newData.credit_balance;
        if (newData.insured_value !== undefined) db[phoneNumber].insured_value = newData.insured_value;
        if (newData.expenses !== undefined) db[phoneNumber].expenses = newData.expenses;
        if (newData.radicado !== undefined) db[phoneNumber].radicado = newData.radicado;
        if (newData.stage !== undefined) db[phoneNumber].stage = newData.stage;
        
        if (newData.consent !== undefined) db[phoneNumber].consent = newData.consent;
        if (newData.is_confirmed !== undefined) db[phoneNumber].is_confirmed = newData.is_confirmed;

        // Añadir al historial
        if (newMessage) {
            db[phoneNumber].history.push({ role: 'user', content: newMessage });
        }
        if (aiReply) {
            db[phoneNumber].history.push({ role: 'assistant', content: aiReply });
        }

        // Mantener el historial acotado a los últimos 20 mensajes para ahorrar tokens
        if (db[phoneNumber].history.length > 20) {
            db[phoneNumber].history = db[phoneNumber].history.slice(-20);
        }

        writeDB(db);
    }
};

module.exports = {
    getUserState,
    updateUserState
};
