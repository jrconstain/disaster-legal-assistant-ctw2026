---
schema_version: 0.1.0
document_id: ctw2026-kb-inmuebles-colombia
jurisdiction: Colombia
last_researched: '2026-08-15'
purpose: Base preliminar para RAG del asistente de afectaciones a inmuebles
warning: Base de trabajo para hackathon; requiere revisión jurídica antes de producción.
---

# Knowledge base preliminar - afectaciones a inmuebles (Colombia)

## Cómo leer esta base

Esta versión conserva el material entregado por el equipo y agrega una sección separada de investigación web. Para que un agente pueda distinguir procedencia, cada bloque usa una etiqueta de origen:

- `ORIGIN: USER_SOURCE` = contenido proveniente de los Markdown suministrados por el equipo. Se conserva como fuente, incluso cuando más adelante se marca una afirmación que requiere revisión.
- `ORIGIN: WEB_ADDED_2026-08-15` = contenido agregado por ChatGPT a partir de fuentes web consultadas el 15 de agosto de 2026.
- `STATUS: VERIFIED_PRIMARY` = verificado contra una fuente normativa u oficial primaria.
- `STATUS: SECONDARY_OR_INSTITUTIONAL` = fuente institucional/sectorial útil, pero no sustituye la norma o el contrato.
- `STATUS: NEEDS_REVIEW` = afirmación que no debe convertirse en regla determinista del agente sin revisión adicional.

## Reglas de uso por el agente

1. No inventar hechos, coberturas, números de póliza, cláusulas o diagnósticos técnicos.
2. Separar `hecho declarado por el usuario`, `observación de una imagen/documento` y `conclusión técnica o jurídica`.
3. La póliza y el contrato concretos tienen prioridad para conocer partes, vigencia, coberturas, deducibles, destinatarios y procedimientos, sin desplazar normas imperativas.
4. Una fotografía puede documentar una grieta, rotura o desprendimiento visible, pero no prueba por sí sola daño estructural o inhabitabilidad.
5. En seguros, distinguir: (a) aviso de ocurrencia; (b) acreditación de ocurrencia; (c) acreditación de cuantía cuando corresponda; (d) decisión de cobertura por la aseguradora.
6. En arrendamiento, no convertir automáticamente cualquier daño en terminación del contrato. La destrucción total tiene una regla específica; los daños parciales exigen analizar hechos, contrato, reparaciones, instrucciones técnicas y normas aplicables.
7. En propiedad horizontal, la obligación legal mínima de seguro recae sobre bienes comunes asegurables frente a incendio y terremoto. No inferir de esa obligación que todos los bienes privados estén cubiertos ni que nunca puedan estarlo: revisar la póliza concreta.

# PARTE I - MATERIAL ENTREGADO POR EL EQUIPO


---

## Fuente del equipo: `AlcaldiaCali_Comunicado_Terremoto_Reporte_Vivienda.md`

**ORIGIN: USER_SOURCE**

---
schema_version: 2.0.0
document_id: reporte-afectaciones-vivienda-terremoto-cali
title: ¿Cómo puede hacer un reporte de afectaciones de su vivienda tras el terremoto?
document_type: comunicado
issuer: Alcaldía de Santiago de Cali
publication_date: '2026-08-14'
event_date: '2026-08-10'
jurisdiction: Santiago de Cali, Valle del Cauca, Colombia
source_file: AlcaldiaCali_Comunicado_Terremoto_Reporte_Vivienda.pdf
source_url: https://www.cali.gov.co/boletines/publicaciones/193687/como-puede-hacer-un-reporte-de-afectaciones-de-su-vivienda-tras-el-terremoto/
topics: [reporte de afectaciones, terremoto, viviendas e infraestructura, gestión del riesgo, Central de Monitoreo]
---

> **COMUNICADO IMPORTANTE:** Estimado(a) ciudadano(a): Dado que el correo contactenos@cali.gov.co está temporalmente fuera de servicio, podemos atenderle a través de cuatro canales, los cuales puede consultar aquí. Clic aquí

# ¿Cómo puede hacer un reporte de afectaciones de su vivienda tras el terremoto?

A través de la Central de Monitoreo, la ciudadanía podrá enviar evidencias y datos clave para consolidar la atención de emergencias.

Los equipos avanzan por diferentes sectores de la ciudad, de acuerdo con el orden de los reportes que se realicen.

## Santiago de Cali, 14 de agosto de 2026

La Alcaldía de Cali, a través de la Secretaría de Gestión del Riesgo de Emergencias y Desastres, mantiene activo un canal de WhatsApp para que la comunidad realice el reporte de afectaciones en viviendas e infraestructura, tras el terremoto que golpeó la ciudad el pasado lunes (10.08.2026).

Los reportes serán centralizados a través de esta línea institucional, con el propósito de agilizar la respuesta de los organismos de socorro.

> “El número de WhatsApp corresponde a la Central de Monitoreo de nuestro organismo distrital y es 310 229 97 08. Aquí podrán reportar todas las afectaciones. Hay que recordar que esto es un número de acopio, más no un número de respuesta”, explicó Ricardo Peñuela, secretario de Gestión del Riesgo.

Para que el reporte sea efectivo y los equipos de emergencia puedan priorizar la atención, el ciudadano debe enviar unos datos indispensables a la línea habilitada. “Deberán incluir las especificaciones del bien inmueble y detallar qué daños tiene, para así nosotros poder, en el censo, mirar las afectaciones”, indicó el funcionario.

En lo que se refiere al censo, añadió que para el Registro Unifamiliar de Emergencias (RUFE) se están haciendo rondas por las viviendas afectadas.

> “El objetivo es poder tomar estos registros y que queden censados de manera oficial en el Registro Único de Damnificados (RUD), de la Unidad Nacional para la Gestión del Riesgo de Desastres. En este momento tenemos un centro de procesamiento, que se está organizando de manera cronológica. Atenderemos en manera de llegada o de prioridades, dependiendo si la afectación es muy alta”, puntualizó el secretario Peñuela.

Para las visitas técnicas, la Secretaría de Gestión del Riesgo de Emergencias y Desastres convocó a ingenieros y arquitectos, que han conformado grupos que recorrerán los predios reportados y, de esta manera, emitirán un informe sobre el estado de los mismos.

## Datos que se deben incluir en el reporte de viviendas o edificaciones

**Registro fotográfico:** imagen clara donde se pueda evidenciar el daño o la situación de afectación en el predio.

**Datos de contacto:** nombre completo de la persona encargada de atender a los equipos de emergencia en el sitio.

**Teléfono:** número de contacto directo y disponible para comunicación inmediata con las autoridades.

**Ubicación exacta:** dirección del inmueble o coordenadas para agilizar el desplazamiento hacia el sitio de la emergencia.

## Recuerde

Línea de WhatsApp oficial 310 229 97 08, Central de Monitoreo de la Secretaría de Gestión del Riesgo de Emergencias y Desastres.

## Le puede interesar…

- Alcaldía de Cali inicia caracterización de familias damnificadas por el sismo mediante el Registro Único de Familias en Emergencia

Alcaldía de Cali

## Comunicaciones Alcaldía de Cali

### Alcaldía de Santiago de Cali  
**NIT:** 890399011-3  
**RUT:** Registro Único Tributario  
**Dirección:** Centro Administrativo Municipal (CAM) Avenida 2 Norte # 10-70, Santiago de Cali - Valle del Cauca - Colombia.  
**Horario atención:** Lunes a jueves: Mañana 8:00 am a 11:30 pm Tarde 2:00 pm a 4:30 pm
Viernes: Mañana 7:30 am a 12:30 pm - Tarde 1:30 pm a 4:30 pm  
**Líneas Locales:** 195
+57 (602) 8856173
+57 (602) 8856174
+57 (602) 8856178  
**Línea Nacional:** 01 8000 222 195  
**Línea Anticorrupción:** 157  
**Notificaciones judiciales:** notificacionesjudiciales@cali.gov.co  
**Tutelas e incidentes:** notificacion.tutelas@cali.gov.co  
**Recepción de facturas electrónicas:** facturaselectronicas@cali.gov.co  
**Código Postal:** 760045

©Copyright 2024 - Todos los derechos reservados Alcaldía Santiago de Cali

Politicas Mapa del sitio Términos y Condiciones



---

## Fuente del equipo: `FASECOLDA_comunicados_12aug-1357.md`

**ORIGIN: USER_SOURCE**

---
schema_version: 2.0.0
document_id: fasecolda-seguros-vivienda-terremoto-2026-08-12
title: ¿Qué seguros protegen su vivienda ante un terremoto? Fasecolda explica
document_type: comunicado
issuer: Federación de Aseguradores Colombianos, Fasecolda
publication_date: '2026-08-12'
event_date: '2026-08-10'
jurisdiction: Colombia
source_file: FASECOLDA_comunicados_12aug-1357.pdf
topics: [seguros de vivienda, terremotos, seguros de copropiedades, crédito hipotecario, reclamaciones de seguros]
---

# COMUNICADO DE PRENSA

Agosto 12 de 2026

# ¿Qué seguros protegen su vivienda ante un terremoto? Fasecolda explica

Fasecolda explica los principales seguros que pueden respaldar a propietarios y copropiedades de bienes inmuebles ante los daños ocasionados por el sismo registrado el pasado 10 de agosto

Los inmuebles con crédito hipotecario cuentan con protección frente a incendio y terremoto.

Los ciudadanos pueden consultar en el RUS (www.rus.com.co) si su edificio o conjunto cuenta con un seguro obligatorio de copropiedades

Bogotá. Ante las afectaciones ocasionadas por el sismo registrado el pasado 10 de agosto, la Federación de Aseguradores Colombianos, Fasecolda, entrega información para que las personas puedan identificar qué seguros protegen sus viviendas y qué deben hacer para reportar los daños.

## Lo que usted debe saber. ¡Ojo! No se deje confundir

1. Lo más importante es la vida, proteja su integridad y la de su familia. Las compañías de seguro están prestas para apoyarlo y atenderlo en el momento en que usted lo necesite.

2. Las personas tienen hasta dos a cinco años a partir de la fecha de ocurrencia del siniestro para presentar su reclamación ante la aseguradora. Esto lo contempla el art.1081 del Código de Comercio. Es conveniente que presenten un primer aviso a la compañía de seguros para que esta les pueda ayudar a mitigar el daño y orientarlas en las acciones que deben tomar para hacer la respectiva reclamación.

> **Texto jurídico citado — ARTÍCULO 1081. <PRESCRIPCIÓN DE ACCIONES>.**
>
> La prescripción de las acciones que se derivan del contrato de seguro o de las disposiciones que lo rigen podrá ser ordinaria o extraordinaria.
> La prescripción ordinaria será de dos años y empezará a correr desde el momento en que el interesado haya tenido o debido tener conocimiento del hecho que da base a la acción.
> La prescripción extraordinaria será de cinco años, correrá contra toda clase de personas y empezará a contarse desde el momento en que nace el respectivo derecho. Estos términos no pueden ser modificados por las partes.

3. Las compañías de seguros y reaseguros cuentan con la solidez técnica y financiera necesaria para responder por las obligaciones derivadas de este tipo de eventos. El sector dispone de reservas suficientes, mecanismos de reaseguro y niveles de solvencia adecuados todo dentro de un marco de regulación y supervisión que respaldan la atención de las reclamaciones de los asegurados.

4. Trabajamos de la mano con la UNGRD (Unidad Nacional de Riesgos de Desastres) entregando información y poniendo a su disposición nuestro sistema de Georeferenciación e identificando los riesgos que podrá atender la industria aseguradora para que el Gobierno Nacional se concentre en la comunidad que no tiene estas coberturas.

5. Todas las compañías de seguro han activado sus protocolos de atención para atender a sus asegurados, encuentre la información de contactos en www.fasec​​olda.com

6. Otros seguros que también pueden brindar protección: además de los seguros relacionados con las edificaciones, un terremoto puede activar otras protecciones, dependiendo de las afectaciones sufridas y de las coberturas contratadas.
Entre ellas se encuentran los seguros de vida, salud, Riesgos Laborales y exequiales, así como pólizas que protegen vehículos, contenidos de la vivienda, entre otros. En todos los casos, la recomendación es verificar las condiciones de la póliza y comunicarse directamente con la compañía aseguradora para recibir orientación.

En el caso de las edificaciones, existen diferentes seguros que pueden brindar protección frente a estos eventos. Por eso, el primer paso es identificar cuál de ellos tiene contratado y comunicarse con la aseguradora correspondiente.

## Seguros que debe tener en cuenta

| Tipo de seguro | ¿Qué protege frente a un terremoto? | ¿Qué hacer si hubo daños? |
| --- | --- | --- |
| Seguro asociado a un crédito hipotecario | Los inmuebles hipotecados a favor de entidades financieras deben estar asegurados contra incendio y terremoto durante la vigencia del crédito. La entidad financiera recibe como indemnización el pago del saldo adeudado y el asegurado la parte excedente del valor del bien asegurado. (Art. 101 EOSF) Decreto 663de 1993 | Comuníquese con la entidad financiera o con la compañía de seguros para reportar la afectación y conocer el procedimiento de reclamación. |
| Seguro obligatorio de bienes comunes | Los edificios y copropiedades sometidos al régimen de propiedad horizontal deben contar con un seguro obligatorio para los bienes comunes<br><br>La protección principal de este seguro es contra frente a incendio y terremoto. (Art. 15. Ley 675 2001) | Comuníquese con el administrador de la copropiedad, quien podrá informar cuál es la aseguradora y activar el proceso correspondiente.<br>Si quiere conocer si su copropiedad cuenta con este seguro, también puede realizar la consulta en el Registro Único de Seguros<br>www.rus.com.co |
| Seguro voluntario de hogar | Permite proteger la vivienda en su cobertura principal contra incendio y terremoto y según el valor asegurado contratado<br>Este seguro puede incluir también coberturas adicionales para contenidos, muebles y enseres, daños causados a equipo eléctrico y electrónico, computadores, televisores, neveras, y bicicletas, entre otros.<br>Las condiciones y valores asegurados dependen de cada póliza. Hay compañías que brindan servicios asistenciales de plomería, cerrajería, cambio de vidrios y hasta médico para el hogar. | Comuníquese directamente con su compañía de seguros, informe lo ocurrido y siga sus indicaciones para presentar la reclamación. |

Audio y Video: Gustavo Morales- presidente ejecutivo de Fasecolda

## MÁS INFORMACIÓN

**INGRID VERGARA CALDERÓN — Vicepresidente de Comunicaciones y Asuntos Corporativos; correo electrónico:** ivergara@fasec​​olda.com  
**INGRID VERGARA CALDERÓN — teléfono:** 601 344 3080 Ext. 1801  
**RAMIRO GÓMEZ — Coordinador de Medios Y Comunicaciones; correo electrónico:** rgomez@fasec​​olda.com  
**RAMIRO GÓMEZ — teléfono:** 601 344 3080 Ext. 1804



---

## Fuente del equipo: `PosseHerreraRuiz_FichaNormativa_Inmobiliario.md`

**ORIGIN: USER_SOURCE**

---
schema_version: 2.0.0
document_id: ficha-informativa-inmobiliaria-terremoto
title: FICHA INFORMATIVA INMOBILIARIA TRAS EL TERREMOTO
document_type: guia
issuer: Posse Herrera Ruiz
jurisdiction: Colombia
source_file: PosseHerreraRuiz_FichaNormativa_Inmobiliario.pdf
source_url: https://www.phrlegal.com
topics: [contratos de arrendamiento, créditos hipotecarios, seguros de vivienda, propiedad horizontal, calamidad pública y subsidios]
---

# FICHA INFORMATIVA INMOBILIARIA TRAS EL TERREMOTO

Guía para personas afectadas por el terremoto

## Contratos de arrendamiento: ¿qué pasa si mi vivienda quedó inhabitable?

Si un terremoto destruye o deja inhabitable el inmueble arrendado, el contrato expira por ministerio de la ley (Art. 2008, numeral 1, Código Civil “C.C “), sin necesidad de preaviso ni declaración judicial.

La razón: al perderse la cosa arrendada por fuerza mayor (Art. 64 C.C.), la obligación del arrendador de proporcionar el goce se extingue, y con ella la obligación del arrendatario de pagar el canon. Ninguna de las partes es responsable ni debe indemnización.

## Derechos principales:

1. Si la vivienda fue destruida totalmente, el contrato expiraría de pleno derecho (Art. 2008, numeral 1, Código Civil) y no procedería indemnización por esta razón para ninguna de las partes porque la causa sería ajena a ambas (fuerza mayor).

2. Si las autoridades ordenaron evacuación o un concepto técnico establece que el inmueble no es habitable, opera el mismo efecto: la imposibilidad de goce extingue la obligación de pago si la evacuación es permanente.

3. No se requiere una cláusula expresa en el contrato, la expiración opera por ministerio de la ley (Art. 2008 C.C.), sin necesidad de pacto adicional.

## Ruta jurídica:

1. Formalizar la expiración del contrato por escrito (constancia de entrega y paz y salvo) tan pronto la situación lo permita, para evitar reclamos futuros.

2. Si el inmueble es reparable (no hubo destrucción total), el arrendador es responsable de ejecutar las reparaciones necesarias para devolverlo a condiciones habitables (Art. 1985 C.C.: las reparaciones necesarias corresponden al arrendador; Art. 1982, numeral 2, C.C.: obligación de mantener la cosa en estado de servir para el fin arrendado).

## Norma aplicable:

1. Código Civil colombiano: Arts. 64, 1496, 1625 (numeral 7), 1729, 1982 (numeral 2), 1985 y 2008 (numeral 1).

2. Ley 820 de 2003, artículo 8, numerales 1 y 2.

## Créditos hipotecarios: ¿qué pasa con la deuda si la vivienda resultó afectada?

Toda vivienda financiada mediante crédito hipotecario o leasing habitacional debe contar con un seguro obligatorio contra incendio y terremoto durante la vigencia de la deuda. Ese seguro puede cubrir los daños e incluso saldar la obligación con la entidad financiera.

## Derechos principales:

La vivienda hipotecada cuenta con un seguro obligatorio contra incendio y terremoto que cubre la parte destructible del inmueble (no el terreno), conforme a la Ley 546 de 1999 [NOTA: eliminar este comentario e incluir donde dice “Ley 546 de 1999”] y el Estatuto Orgánico del Sistema Financiero.

## Pasos a seguir:

1. Dar aviso de siniestro a la aseguradora en un plazo de 3 días hábiles desde la fecha del siniestro, o, de no ser posible, en el menor plazo posible. Este aviso se puede realizar telefónicamente o por escrito.

2. Notificar simultáneamente a la entidad financiera sobre el siniestro y solicitar instrucciones para la activación de la póliza.

3. Documentar los daños con fotos y videos (sin exponerse a riesgos) y allegar los demás documentos requeridos por la entidad financiera y la aseguradora.

## Normal aplicable:

1. Ley 546 de 1999 (sistema de financiación de vivienda).

2. Estatuto Orgánico del Sistema Financiero (seguro obligatorio de incendio y terremoto para inmuebles financiados).

3. Circular Básica Financiera de la Superintendencia Financiera de Colombia.

## Póliza de zonas comunes en propiedad horizontal (conjuntos y edificios)

Todos los conjuntos residenciales y edificios sometidos a propiedad horizontal deben contar con un seguro obligatorio que protege las áreas compartidas (estructura, fachadas, ascensores, cubiertas, etc.) contra terremoto. Este seguro NO cubre las unidades privadas (apartamentos) por dentro.

## Derechos principales:

1. La póliza de bienes comunes es obligatoria para toda propiedad horizontal. Debe cubrir los bienes comunes susceptibles de ser asegurados contra incendio y terremoto (Art. 15, parágrafo 1, Ley 675 de 2001).

2. Cubre: estructura, cimientos, fachadas, cubiertas, ascensores, zonas sociales y demás áreas comunes susceptibles de destruirse por el siniestro.

3. NO cubre: el interior de las unidades privadas, muebles, electrodomésticos ni acabados de cada propietario.

4. La indemnización debe destinarse primero a la reconstrucción del edificio o conjunto, si el inmueble no es reconstruido el importe se distribuye entre propietarios según el coeficiente de copropiedad (Art. 15, parágrafo 2, Ley 675 de 2001).

2. ¿Quién gestiona el seguro? el administrador del edificio o conjunto es responsable de contratar y mantener vigente la póliza, y de reportar el siniestro ante la aseguradora (Art. 51, numeral 7, Ley 675 de 2001).

## ¿Quién gestiona el seguro?

El administrador del edificio o conjunto es responsable de contratar y mantener vigente la póliza, y de reportar el siniestro ante la aseguradora (Art. 51, numeral 7, Ley 675 de 2001).

## Norma aplicable

Ley 675 de 2001, artículo 15, parágrafos 1 y 2 y artículo 51.

# Declaratoria de calamidad pública y subsidios del gobierno

El Gobierno Nacional ha declarado calamidad pública y desastre nacional. Esto permite activar ayudas, subsidios y mecanismos de emergencia para los afectados.

## ¿Qué se ha decretado?

1. Declaratoria de calamidad pública en el Valle del Cauca por 6 meses (Decreto 1.03.01-1070 de 2026), con base en la Ley 1523 de 2012.

2. Declaratoria de desastre nacional por el Presidente de la República.

3. Declaratoria de emergencia económica nacional para crear el Fondo Milagro destinado a la reconstrucción.

## Ayudas anunciadas

1. Subsidio de arriendo temporal para familias damnificadas que no pueden habitar su vivienda.

2. Alivio en servicios públicos por tres meses para afectados en Risaralda (y se espera extensión a otras zonas).

3. Programa de reconstrucción de viviendas a través de la UNGRD y el Ministerio de Vivienda.

## Requisitos para acceder (Ley 1523 de 2012 y protocolos UNGRD):

1. “Ley 1523 de 2012”

2. Estar inscrito en el censo oficial de damnificados realizado por la alcaldía local.

3. Estar registrado en el Registro Único de Damnificados (RUD) de la UNGRD.

## Norma aplicable

1. Ley 1523 de 2012 (Política Nacional de Gestión del Riesgo de Desastres), artículos 57-65.



# PARTE II - ADICIONES DE INVESTIGACIÓN WEB (CHATGPT, 2026-08-15)

> **IMPORTANTE:** Todo lo que aparece en esta Parte II fue agregado por ChatGPT después de consultar fuentes web. No proviene de los tres Markdown originales.

## WEB-INS-1068 - Código de Comercio, artículo 1068

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Secretaría del Senado / Gestor Normativo de Función Pública
- URL primaria: https://www.secretariasenado.gov.co/senado/basedoc/codigo_comercio_pr032.html
- Uso para el agente: **no usar este artículo como fundamento del aviso o reclamación de un siniestro**.
- Regla resumida: el artículo 1068 trata la mora en el pago de la prima y sus efectos sobre el contrato de seguro. Por tanto, una referencia a “art. 1068 = carta de reclamación” es incorrecta.

## WEB-INS-1075 - Aviso de ocurrencia del siniestro

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Código de Comercio, art. 1075
- URL primaria: https://www.secretariasenado.gov.co/senado/basedoc/codigo_comercio_pr033.html
- Regla resumida: el asegurado o beneficiario debe dar noticia de la ocurrencia al asegurador dentro de los tres días siguientes a aquel en que conoció o debió conocer el siniestro; las partes pueden ampliar ese plazo, no reducirlo.
- Uso para el agente: si el usuario aún no tiene cotizaciones o cuantía completa, puede ser útil preparar **un aviso inicial** con identificación, póliza, fecha/evento, inmueble y descripción/evidencia disponible, sin afirmar que la reclamación completa ya está acreditada.
- Precaución: la ley habla de “tres días siguientes”; esta base no debe convertirlo automáticamente en “tres días hábiles”.

## WEB-INS-1077 - Carga de acreditar ocurrencia y cuantía

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Código de Comercio, art. 1077
- URL primaria: https://www.secretariasenado.gov.co/senado/basedoc/codigo_comercio_pr033.html
- Regla resumida: corresponde al asegurado demostrar la ocurrencia del siniestro y, cuando sea el caso, la cuantía de la pérdida; al asegurador le corresponde demostrar hechos o circunstancias excluyentes de responsabilidad.
- Uso para el agente: clasificar cada soporte según si ayuda a probar `ocurrencia`, `daño`, `cuantía`, `identidad/interés asegurable` o `canal/procedimiento`.

## WEB-INS-SFC-LIBERTAD-PRUEBA - Libertad probatoria en reclamaciones

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY (criterio institucional/jurisdiccional de la SFC)
- Tipo: doctrina/jurisprudencia administrativa
- Fuente: Superintendencia Financiera de Colombia - Contrato de seguro / jurisprudencia histórica
- URL: https://www.superfinanciera.gov.co/publicaciones/10085296/
- Regla resumida: la SFC ha reiterado que la ocurrencia y cuantía pueden acreditarse mediante medios probatorios idóneos y pertinentes; no debe modelarse el flujo como si una única lista cerrada de documentos fuera la única forma jurídicamente posible de probar el siniestro.
- Uso para el agente: una póliza puede pedir soportes y la aseguradora puede solicitar información pertinente, pero el asistente debe distinguir entre `documentos recomendados/requeridos por canal` y la regla general de acreditación probatoria.

## WEB-INS-1080 - Pago u objeción después de la reclamación acreditada

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Código de Comercio, art. 1080, modificado por Ley 510 de 1999
- URL primaria: https://www.secretariasenado.gov.co/senado/basedoc/ley_0510_1999_pr002.html
- Regla resumida: el término legal para el pago se relaciona con el momento en que el asegurado o beneficiario acredita su derecho conforme al artículo 1077, no simplemente con el primer mensaje de aviso.
- Uso para el agente: no prometer fechas de pago a partir de la mera notificación inicial.

## WEB-INS-1081 - Prescripción de acciones del contrato de seguro

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Código de Comercio, art. 1081
- URL primaria: https://www.secretariasenado.gov.co/senado/basedoc/codigo_comercio_pr033.html
- Regla resumida: existe prescripción ordinaria y extraordinaria con términos y puntos de inicio diferentes. El comunicado de Fasecolda suministrado por el equipo resume esta regla como un horizonte de dos a cinco años, pero el agente no debe presentar esos términos como si fueran un plazo único para dar el aviso inicial del art. 1075.

## WEB-INS-EOSF-101 - Inmuebles hipotecados y seguro de incendio/terremoto

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma + criterio institucional
- Fuente normativa: Estatuto Orgánico del Sistema Financiero (Decreto 663 de 1993), art. 101, num. 1
- URL normativa: https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=1348
- Fuente complementaria: Superintendencia Financiera de Colombia, jurisprudencia de contrato de mutuo
- URL complementaria: https://www.superfinanciera.gov.co/publicaciones/10085297/
- Regla resumida: los inmuebles hipotecados a favor de entidades vigiladas por la SFC deben estar asegurados contra incendio y terremoto. El agente debe ayudar a localizar la póliza y revisar sus condiciones; no debe inventar aseguradora, suma asegurada, beneficiario ni alcance.

## WEB-PH-LEY675-15 - Seguros en propiedad horizontal

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Ley 675 de 2001, art. 15
- URL primaria: https://www.secretariasenado.gov.co/senado/basedoc/ley_0675_2001.html
- Regla resumida: es obligatoria la constitución de pólizas contra incendio y terremoto sobre los bienes comunes susceptibles de ser asegurados. La ley permite además pólizas orientadas a garantizar reconstrucción total.
- Uso para el agente: `common_property_insurance_possible = true` cuando el inmueble pertenece a propiedad horizontal; pedir póliza o contacto de administración. No inferir cobertura concreta de unidades privadas sin leer la póliza.

## WEB-RENT-LEY820-BASE - Contenido mínimo y obligaciones del arrendamiento de vivienda urbana

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Ley 820 de 2003
- URL: https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=8738
- Puntos útiles para extracción documental:
  - El contrato puede ser verbal o escrito, pero las partes deben acordar datos mínimos como identificación de contratantes e inmueble, parte arrendada cuando aplique, precio/forma de pago, servicios o usos relacionados, término y responsables de servicios públicos.
  - El arrendador tiene obligaciones de entrega y mantenimiento en condiciones aptas para el uso pactado y, si el contrato consta por escrito, de entrega de copias en los términos legales.
  - El arrendatario debe pagar el canon, cuidar el inmueble y asumir las reparaciones imputables a su mal uso o culpa, entre otras obligaciones.
  - El reajuste del canon de vivienda urbana se sujeta al art. 20 y no puede hacerse arbitrariamente antes de completar el periodo legal.

## WEB-RENT-LEY820-16 - Prohibición de depósitos y cauciones reales

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Ley 820 de 2003, art. 16
- URL: https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=8738
- Regla resumida: en arrendamiento de vivienda urbana no se pueden exigir depósitos en dinero efectivo u otras cauciones reales para garantizar las obligaciones generales del arrendatario, con el régimen especial aplicable a servicios públicos.
- Fuente institucional complementaria (2026): Secretaría Distrital del Hábitat de Bogotá, concepto jurídico sobre depósitos/“estimativos”.
- URL: https://habitatbogota.gov.co/sites/default/files/marco-legal/2026-07/3-2025-11218_1%20-%20CONCEPTO%20JUR%C3%8DDICO%20SOBRE%20LA%20INTERPRETACI%C3%93N%20Y%20APLICACI%C3%93N%20DEL%20ART%C3%8DCULO%2015%20DE%20LA%20LEY%20820%20DE%202003..pdf

## WEB-RENT-CC-1982-1985-2008 - Goce, reparaciones y destrucción total

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: norma
- Fuente primaria: Código Civil, régimen de arrendamiento de cosas
- URLs: https://www.secretariasenado.gov.co/senado/basedoc/codigo_civil_pr061.html y https://www.secretariasenado.gov.co/senado/basedoc/codigo_civil_pr062.html
- Regla de uso para el agente:
  - Arts. 1982 y 1985 son relevantes para la obligación de mantener la cosa en estado de servir para el fin arrendado y para reparaciones necesarias, con las excepciones legales.
  - Art. 2008 contempla la expiración del arrendamiento por destrucción total de la cosa arrendada.
  - **Guardrail:** no equiparar automáticamente `grieta`, `evacuación preventiva`, `daño parcial` o `falta de informe técnico` con `destrucción total`.

## WEB-EMERG-VALLE-1070-2026 - Calamidad pública Valle del Cauca

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: VERIFIED_PRIMARY
- Tipo: acto administrativo vigente/relevante al evento
- Fuente: Gobernación del Valle del Cauca, Decreto 1.03.01-1070 de 2026, 10 de agosto de 2026
- URL: https://valledelcauca.gov.co/loader.php?idHash=sxzFEfKHxHvmQ34iZ_wJtDppS2YxSDNqWA&lFuncion=visorpdf&lServicio=Tools2&lTipo=descargas&pdf=1
- Regla resumida: el departamento declaró situación de calamidad pública a raíz del sismo. Esta fuente puede usarse para contexto de emergencia, pero no sustituye requisitos individuales para seguros, arrendamientos, censos o subsidios.

## WEB-POLICY-REFERENCE-ALLIANZ-HOGAR - Referencia de estructura contractual de póliza

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: SECONDARY_OR_INSTITUTIONAL
- Tipo: condiciones generales de producto real, usadas solo como referencia de estructura
- Fuente: Allianz Colombia - Seguro de Hogar, condiciones generales (versión publicada en sitio oficial)
- URL: https://www.allianz.co/content/dam/onemarketing/iberolatam/allianz-co/seguros/personas/hogar/2021/Hogar-Individual-13122023-Version-24.pdf
- Rasgos útiles para fixtures: separación de exclusiones/amparos, definición de bienes, amparo de terremoto, tratamiento de eventos sísmicos dentro de 72 horas, obligaciones del asegurado y cláusulas genéricas.
- Restricción: no copiar textualmente el clausulado ni asumir que sus deducibles o coberturas aplican a otra póliza.

## WEB-POLICY-REFERENCE-SURA-HOGAR - Segunda referencia de producto

- ORIGIN: WEB_ADDED_2026-08-15
- STATUS: SECONDARY_OR_INSTITUTIONAL
- Tipo: condiciones generales / información de producto
- Fuente: Seguros SURA Colombia - Seguro de Hogar
- URLs: https://www.segurossura.com.co/documentos/condicionados/personas/hogar/condicionado-hogar-sura-plus-valor-comercial.pdf y https://www.segurossura.com.co/paginas/hogar/hogar-sura.aspx
- Rasgos útiles: cobertura de eventos naturales condicionada al producto contratado; límites, exclusiones, asistencias y gasto adicional pueden variar. Siempre leer carátula y condiciones particulares.

# PARTE III - NOTAS DE REVISIÓN / POSIBLES CONFLICTOS

## REVIEW-001 - Artículo 1068

- STATUS: NEEDS_REVIEW en cualquier prompt/documento que diga que el art. 1068 regula la reclamación.
- Corrección: la regla del aviso está en el art. 1075; el art. 1068 trata mora en pago de prima.

## REVIEW-002 - “Tres días hábiles” en la ficha Posse Herrera Ruiz

- STATUS: NEEDS_REVIEW
- La ficha del equipo dice “3 días hábiles”. El texto legal del art. 1075 se refiere a tres días siguientes y no debe transformarse sin fundamento adicional en “hábiles”. Para generación, usar la formulación legal o la que amplíe la póliza concreta.

## REVIEW-003 - Inhabitabilidad / evacuación y terminación automática

- STATUS: NEEDS_REVIEW
- La ficha Posse Herrera Ruiz formula de manera amplia que una orden de evacuación o concepto de inhabitabilidad puede producir el mismo efecto que la destrucción total. Para el MVP, esa proposición no debe codificarse como regla determinista. Debe analizarse el carácter temporal/permanente, el grado de destrucción, el contrato, las reparaciones y la fuente jurídica aplicable.

## REVIEW-004 - Bienes privados en propiedad horizontal

- STATUS: NEEDS_REVIEW
- La obligación mínima de la Ley 675 art. 15 recae sobre bienes comunes asegurables. Decir que una póliza de copropiedad “NO cubre” en ningún caso unidades privadas es demasiado categórico: la cobertura efectiva depende del contrato y de amparos adicionales que la copropiedad haya contratado. El agente debe leer la póliza.

## REVIEW-005 - Declaratorias nacionales y “Fondo Milagro” de la ficha del equipo

- STATUS: NEEDS_REVIEW para uso jurídico automatizado
- El material del equipo contiene afirmaciones sobre desastre nacional, emergencia económica y Fondo Milagro. Para esta versión se verificó de forma primaria la calamidad pública del Valle del Cauca, pero no se incorporó como fuente normativa primaria un decreto nacional específico dentro de esta base. Antes de usar esas afirmaciones para crear derechos, plazos o trámites, incorporar y versionar el acto nacional correspondiente.

# PARTE IV - MAPA DE FUENTES PARA GENERACIÓN

| source_id | Tema | Prioridad para generación |
|---|---|---|
| WEB-INS-1075 | Aviso de siniestro | Alta |
| WEB-INS-1077 | Ocurrencia y cuantía | Alta |
| WEB-INS-1080 | Pago después de acreditar derecho | Alta |
| WEB-INS-1081 | Prescripción | Media |
| WEB-INS-EOSF-101 | Seguro hipotecario | Alta cuando `has_credit=true` |
| WEB-PH-LEY675-15 | Seguro de bienes comunes | Alta cuando `building_type` indica PH |
| WEB-RENT-LEY820-BASE | Contrato de vivienda urbana | Alta en arrendamiento |
| WEB-RENT-LEY820-16 | Depósitos/cauciones | Baja para desastre, alta para revisión contractual |
| WEB-RENT-CC-1982-1985-2008 | Reparaciones/destrucción total | Alta en afectación del inmueble arrendado |
| AlcaldiaCali... | Canal/censo local post-sismo | Alta si ubicación=Cali y contexto=2026-08 |
| FASECOLDA... | Orientación sectorial post-sismo | Media/alta para explicar rutas |
| PosseHerreraRuiz... | Guía jurídica secundaria | Media; aplicar REVIEW-002/003/004/005 |

