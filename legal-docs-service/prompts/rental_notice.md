# RUTA ESPECIFICA - COMUNICACION DE AFECTACION EN ARRENDAMIENTO

Genera un `rental_damage_notice` dirigido al arrendador o inmobiliaria identificados en el expediente.

## Objetivo del documento

La carta debe dejar constancia oportuna de que ocurrio un sismo, que se presentaron determinadas afectaciones y que, por el estado reportado del inmueble y/o las instrucciones preventivas disponibles, la persona arrendataria no ha podido continuar normalmente con el uso y goce residencial pactado.

No declares automaticamente terminado el contrato. No afirmes que "el inmueble es inhabitable" salvo que exista soporte tecnico o de autoridad que realmente diga eso. Cuando el caso solo tenga fotos e instruccion preventiva, explica que el retorno esta pendiente de evaluacion, reparacion o habilitacion.

## Subsunccion obligatoria

Incluye `legal_reasoning` aplicando explicitamente la estructura:

- la regla o clausula establece el objeto de uso/goce y las obligaciones de mantenimiento/reparacion pertinentes;
- en el caso concreto, describe que ocurrio y por que actualmente no puede ejercerse normalmente ese uso/goce;
- por consiguiente, formula la medida contractual solicitada.

La consecuencia debe redactarse como una solicitud proporcionada al soporte del expediente. Entre las medidas utiles estan: evaluacion, reparacion/habilitacion, respuesta escrita y definicion del tratamiento del canon durante el periodo en que el uso residencial no ha sido posible. Si las fuentes y hechos lo permiten, solicita que no se continue facturando el canon como si el inmueble estuviera disponible para su destinacion ordinaria; no conviertas esa solicitud en una afirmacion categorica de terminacion automatica.

## Notificaciones

Incluye obligatoriamente en `notifications` los datos de la arrendataria y del destinatario que aparezcan en el contrato, en particular el capitulo/clausula de notificaciones, o en el CASE_JSON.
