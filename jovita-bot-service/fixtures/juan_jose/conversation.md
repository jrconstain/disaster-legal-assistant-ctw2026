# Escenario E2E — Juan José Rojas Constaín

Fixture conversacional para probar **Jovita localmente sin WhatsApp**. Los bloques `jovita-turn` son machine-readable y `scripts/replay_markdown.py` los reproduce uno por uno. Los adjuntos usan rutas locales relativas a la raíz de `jovita-bot-service/`.

> Todos los documentos, compañías, números y canales de este fixture son sintéticos y solo sirven para pruebas CTW 2026.

## U01 — Juan inicia el chat

```jovita-turn
type: text
text: "Hola"
attachments: []
```

### Jovita — esperado

Hola 👋 Soy Jovita, una IA que te ayuda si tu inmueble sufrió daños por un sismo, inundación, deslizamiento u otra emergencia.

Puedo revisar contratos o pólizas, organizar tus evidencias y ayudarte a preparar una reclamación o comunicación y explicarte cómo radicarla. 📄

Para empezar, cuéntame tu caso como te salga, por texto o nota de voz: dónde queda📍, si eres propietario o arrendatario 🏠, qué pasó y qué daños hubo 💥. Si eres propietario, dime también si tienes seguro, pagas un crédito o vives en un edificio o conjunto.

📎 Puedes enviarme fotos, videos o documentos. Si no tienes todo claro, no te preocupes que yo te iré guiando.

Después envía el consentimiento con botones `consent_yes` / `consent_no`.

---

## U02 — Juan autoriza tratamiento de datos

```jovita-turn
type: button
text: "consent_yes"
attachments: []
```

### Jovita — esperado

Confirma la autorización y le pide que cuente el caso libremente. No llama al LLM antes del consentimiento.

---

## U03 — Relato inicial libre

```jovita-turn
type: text
text: |
  Ahorita, imagínate que, pues yo tengo, pues tenía mi apartamento en el conjunto Villas de Guadalupe. Eso es la carrera 56, número 14-57, el apartamento 402. Yo soy el dueño, pues la verdad, yo no me acuerdo de haberle comprado ningún seguro, pero pues todavía lo estoy pagando con Bancolombia, el crédito hipotecario. Llevo pagando 12 años, me faltan ocho. La verdad es que la casa quedó destruida, se cayeron partes del techo, paredes, se me destruyeron muchos objetos, quedó inhabitable prácticamente. Y bueno, la verdad no sé qué hacer. Soy Juan José Rojas. Mi cédula es 1-113-682-988.
attachments: []
```

### Extracción esperada al `case.json`

- `ownership_status = owner`
- `location.address = Carrera 56 # 14-57, Apartamento 402`
- `location.property_name = Villas de Guadalupe`
- `has_credit = true`
- `credit.bank = Bancolombia`
- `has_insurance = null` por ahora: “no recuerdo haber comprado seguro” no cierra la ruta cuando existe crédito hipotecario.
- `building_type = apartment_in_horizontal_property`
- `event.type` queda pendiente en este turno: Juan todavía no nombra explícitamente el sismo/terremoto en su relato. Se completa en U06.
- daños reportados en techo, paredes y contenidos.
- `event.user_reports_uninhabitable = true`, sin convertirlo en dictamen técnico.

### Jovita — esperado

Explica que el crédito abre una ruta para localizar póliza. Pide la póliza/certificado en PDF y dice que puede mandar fotos desde ya. No asegura cobertura.

---

## U04 — Juan encuentra y envía la póliza

```jovita-turn
type: text
text: "Encontré esta póliza. Creo que debe ser la del apartamento."
attachments:
  - path: fixtures/juan_jose/poliza_hogar_sintetica_juan_jose_rojas_constain.pdf
    kind: document
    mime_type: application/pdf
    filename: poliza_hogar_sintetica_juan_jose_rojas_constain.pdf
```

### Extracción esperada del PDF

- asegurado: **Juan José Rojas Constaín**
- C.C. `1-113-682-988`
- póliza `HOG-2026-0081640`
- aseguradora sintética `Seguros Horizonte Andino S.A.`
- inmueble asegurado: Carrera 56 # 14-57, apartamento 402, Villas de Guadalupe, Cali.
- vigencia 20/01/2026–20/01/2027.
- existe amparo de terremoto/temblor para edificación y contenidos, con límites y deducible descritos en la póliza.
- **No** inferir que el siniestro concreto ya fue aceptado.
- guardar el PDF y su ruta local dentro de `documents[]`.
- registrar como warning que la póliza sintética dice “hipoteca no declarada”, mientras Juan reportó crédito con Bancolombia; esto no impide usar la póliza si identidad e inmueble coinciden.

### Jovita — esperado

Da un parte de tranquilidad prudente: encontró una póliza que coincide y un amparo relacionado con terremoto; por tanto ya hay una ruta concreta para avisar el siniestro, pero la aseguradora deberá decidir cobertura. Pide fotos/videos.

---

## U05 — Juan envía tres fotos

```jovita-turn
type: text
text: "Estas son las fotos que pude tomar de cómo quedó el apartamento y el edificio."
attachments:
  - path: fixtures/juan_jose/evidence/evidence_01_interior.jpg
    kind: image
    mime_type: image/jpeg
  - path: fixtures/juan_jose/evidence/evidence_02_escombros.jpg
    kind: image
    mime_type: image/jpeg
  - path: fixtures/juan_jose/evidence/evidence_03_fachada.jpg
    kind: image
    mime_type: image/jpeg
```

### Extracción esperada

Se crean `E-01`, `E-02`, `E-03` con:

- ruta local persistida;
- descripción visual prudente;
- `model_observation` separado del relato del usuario;
- `technical_conclusion = null`.

Las fotos muestran desprendimientos/mampostería dañada, escombros interiores y afectación visible de fachada, pero **Jovita no certifica daño estructural ni habitabilidad**.

### Jovita — esperado

Confirma que guardó tres evidencias y pide el dato que aún bloquea el aviso: fecha del evento/fecha en que conoció los daños y, si existe, hora aproximada. Pregunta también si hubo gastos o reparaciones provisionales.

---

## U06 — Juan completa fecha y estado de gastos

```jovita-turn
type: text
text: |
  Fue el terremoto del 10 de agosto de 2026, como a las 7:34. Yo vi los daños ese mismo día. No he hecho reparaciones ni he pagado nada todavía y tampoco tengo una cotización completa.
attachments: []
```

### Jovita — esperado

El caso queda listo para ofrecer la generación del **aviso inicial descriptivo del siniestro**, sin cuantificar la reclamación y sin esperar una cotización completa.

---

## U07 — Juan pide generar

```jovita-turn
type: text
text: "Sí, hagámoslo"
attachments: []
```

### Jovita — esperado

Muestra un resumen construido desde el `case.json` con nombre, cédula, inmueble, póliza, aseguradora, evento, daños y número de fotos. Envía botones:

- `confirm_yes` — ✅ Confirmar
- `confirm_correct` — ✏️ Corregir

Todavía **no** dispara `legal-docs-service`.

---

## U08 — Juan confirma el expediente

```jovita-turn
type: button
text: "confirm_yes"
attachments: []
```

### Resultado esperado

1. `is_confirmed = true`.
2. `claim.status = ready_to_generate` y luego `generated` si termina bien.
3. El `case.json` final se persiste.
4. Jovita invoca el `legal-docs-service` hermano con:
   - el `case.json` final;
   - el knowledge base fijo que ya vive dentro de `legal-docs-service`;
   - los paths locales de póliza y fotos ya referenciados dentro del JSON.
5. El servicio genera el PDF.
6. En WhatsApp, Jovita sube y envía ese PDF como documento.

## Comandos de replay

Sin llamadas externas y sin generar el PDF jurídico:

```powershell
python scripts/replay_markdown.py --provider mock --skip-docs
```

Con OpenAI para extracción multimodal, pero sin WhatsApp:

```powershell
python scripts/replay_markdown.py --provider openai --skip-docs
```

E2E local incluyendo el servicio jurídico hermano con sus mocks:

```powershell
python scripts/replay_markdown.py --provider mock --legal-docs-provider mock
```

E2E real usando GPT-5.6 Luna tanto en Jovita como en el generador jurídico:

```powershell
python scripts/replay_markdown.py --provider openai --legal-docs-provider openai
```
