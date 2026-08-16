# Comentarios de abogados incorporados

Este repo simplificado ajusta los prompts y el renderer con base en los comentarios entregados al equipo el 15 de agosto de 2026.

## Abogado 1 - subsuncion

Se incorporo una estructura obligatoria de subsuncion para documentos que requieren razonamiento juridico:

1. regla/norma aplicable;
2. hechos del caso que encajan en la regla;
3. consecuencia o solicitud juridica.

En el schema esto corresponde a `LegalReasoningStep(rule, case_application, conclusion, source_ids, citation_text)`.

## Abogado 1 - notificaciones

Se agrego una seccion final obligatoria `Notificaciones y datos de contacto`. El LLM debe extraer del caso o de los documentos los correos, direcciones y telefonos disponibles para remitente y destinatario. El renderer la incluye siempre que exista informacion.

## Abogado 2 - seguro

El primer documento de seguros se redefine como `insurance_loss_notice`, no como reclamacion completa. El prompt exige:

- documento descriptivo;
- sin capitulo de fundamento juridico;
- sin cuantificar gastos/perdidas;
- sin acreditar aun facturas o cotizaciones;
- identificacion, poliza, inmueble, evento, afectaciones y fotos;
- solicitud simple de recepcion y canal/numero para seguimiento.

El validador rechaza drafts de seguro que incluyan `legal_reasoning` o intenten convertir el aviso inicial en una exigencia de indemnizacion cuantificada.

## Abogado 2 - arrendamiento

La carta explica el vinculo entre el objeto del arrendamiento (uso/goce residencial), los hechos posteriores al sismo y la necesidad de evaluacion/reparacion/habilitacion. El prompt pide solicitar una definicion contractual del canon durante el periodo en que no ha sido posible ejercer normalmente el uso residencial, sin afirmar terminacion automatica ni certificar inhabitabilidad sin soporte tecnico.

Las capturas originales entregadas por el equipo estan en `docs/lawyer_feedback/`.
