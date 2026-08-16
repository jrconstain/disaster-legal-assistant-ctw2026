import React from 'react';

export default function DataPolicy() {
  return (
    <section className="section" style={{ minHeight: '80vh', paddingTop: '4rem' }}>
      <div className="container">
        <h1>Política de Datos y Uso</h1>
        <span className="eyebrow">Transparencia y privacidad</span>
        
        <div style={{ marginTop: '2rem', maxWidth: 'var(--reading-w)' }}>
          <h3 className="mb-2">Marco Legal y Autorización</h3>
          <p>
            En estricto cumplimiento del <strong>Artículo 15 de la Constitución Política de Colombia</strong>, la <strong>Ley Estatutaria 1581 de 2012</strong> (Ley General de Protección de Datos Personales o <em>Habeas Data</em>), el Decreto 1377 de 2013 y demás normas que los modifiquen o reglamenten, garantizamos el derecho fundamental de los usuarios a conocer, actualizar, rectificar y suprimir la información personal recopilada. Al interactuar con el asistente Jovita (un MVP en contexto de hackathon), usted otorga su autorización previa, expresa e informada para el tratamiento temporal de sus datos bajo estos términos.
          </p>

          <h3 className="mb-2 mt-8">¿Qué datos recolectamos?</h3>
          <p>
            Para poder asistirle adecuadamente en la estructuración de su caso, recolectamos de manera temporal:
          </p>
          <ul>
            <li><strong>Datos de contacto:</strong> Su número de teléfono (necesario para la comunicación vía WhatsApp).</li>
            <li><strong>Historial de interacción:</strong> Los mensajes de texto y notas de voz generados durante su conversación con el asistente.</li>
            <li><strong>Documentos legales y de identificación:</strong> Archivos que usted envíe voluntariamente para sustentar su caso. Esto incluye, pero no se limita a, copias de la Cédula de Ciudadanía u otros documentos de identidad, contratos de arrendamiento, pólizas de seguros, certificados de tradición y libertad, extractos de créditos hipotecarios y facturas.</li>
            <li><strong>Evidencia multimedia:</strong> Fotografías o videos de las afectaciones al inmueble.</li>
          </ul>

          <h3 className="mb-2 mt-8">Tratamiento Especial de Datos Sensibles y Documentos</h3>
          <p>
            Entendemos la naturaleza crítica y confidencial de los documentos que usted comparte (como cédulas y pólizas). En estricto apego a la ley, declaramos que:
          </p>
          <ul>
            <li><strong>Facultatividad:</strong> Usted no está legalmente obligado a suministrar datos sensibles. Sin embargo, proporcionar esta información permite que el asistente extraiga los datos exactos (nombres, números de póliza, direcciones) necesarios para redactar correctamente la reclamación o comunicación.</li>
            <li><strong>Procesamiento aislado:</strong> Los documentos financieros y legales son procesados mediante Inteligencia Artificial exclusivamente para la extracción de entidades clave asociadas a su caso. </li>
          </ul>

          <h3 className="mb-2 mt-8">¿Cómo utilizamos su información?</h3>
          <p>
            Los datos son procesados exclusivamente para:
          </p>
          <ul>
            <li>Determinar la ruta de atención correspondiente a su caso.</li>
            <li>Extraer información clave para evitar preguntas repetitivas.</li>
            <li>Generar documentos y guías de acción (como reclamaciones o solicitudes).</li>
          </ul>
          <p>
            Nuestros modelos de lenguaje (LLMs) procesan su información para entender su situación y ayudarle. Sus datos <strong>no</strong> son utilizados para entrenar modelos públicos ni se comparten con terceros con fines comerciales.
          </p>

          <h3 className="mb-2 mt-8">Sus Derechos (Habeas Data) y Procedimiento para Borrar sus Datos</h3>
          <p>
            En ejercicio de sus derechos legales como titular de la información (conocer, actualizar, rectificar y solicitar la supresión de sus datos consagrados en la Ley 1581 de 2012), y dada la naturaleza de este MVP, usted tiene control absoluto sobre su información.
          </p>
          <p>
            Hemos diseñado un procedimiento (mock-up) automatizado y sin fricciones para la eliminación inmediata de sus datos. Para solicitar la purga de su información:
          </p>
          <ol style={{ paddingLeft: '1.5rem', marginBottom: '1rem', marginTop: '1rem' }}>
            <li style={{ marginBottom: '0.5rem' }}>Abra el chat de WhatsApp donde ha estado interactuando con Jovita.</li>
            <li style={{ marginBottom: '0.5rem' }}>Envíe el mensaje exacto: <strong>"Por favor, borrar mis datos"</strong>.</li>
            <li style={{ marginBottom: '0.5rem' }}>El sistema procesará la solicitud de inmediato.</li>
            <li style={{ marginBottom: '0.5rem' }}>Recibirá un mensaje de confirmación indicando que su caso ha sido cerrado y que todo su historial de mensajes, documentos legales (cédulas, pólizas), fotografías y audios han sido purgados de forma permanente de nuestra base de datos.</li>
          </ol>

          <h3 className="mb-2 mt-8">Límites y Responsabilidad (Aviso Legal)</h3>
          <p>
            Jovita es un experimento tecnológico y <strong>no constituye asesoría legal, técnica o profesional</strong>. No diagnosticamos daños, ni garantizamos indemnizaciones. Las respuestas y documentos generados son ayudas de redacción y deben ser revisados bajo su propio criterio antes de ser utilizados.
          </p>
        </div>
      </div>
    </section>
  );
}
