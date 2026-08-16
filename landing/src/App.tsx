import NavBar from './components/NavBar';
import DemoHero from './components/DemoHero';
import { getWhatsAppUrl, GITHUB_URL } from './config';

export default function App() {
  return (
    <>
      <NavBar />
      <DemoHero />

      {/* Qué es Jovita */}
      <section className="section">
        <div className="container">
          <span className="eyebrow">Jovita</span>
          <h2>Una conversación que termina en un siguiente paso</h2>
          <p>
            Jovita es una IA conversacional que funciona en WhatsApp para personas cuyo inmueble fue afectado por un desastre. Entiende el relato, lee documentos y evidencia, identifica la ruta relevante y ayuda a producir algo que la persona pueda usar: una comunicación, una reclamación, un expediente de evidencias o una guía concreta de siguientes pasos.
          </p>
          <p>
            El demo actual está concentrado en afectaciones por terremoto. La arquitectura está pensada para extender la misma experiencia a otros desastres que afecten inmuebles.
          </p>
        </div>
      </section>

      {/* Cómo funciona */}
      <section id="como-funciona" className="section" style={{ backgroundColor: '#f5f5f5' }}>
        <div className="container">
          <h2>Cómo funciona</h2>
          
          <div className="mt-8">
            <h3 className="mb-2">01 — Cuéntale qué pasó</h3>
            <p>No empiezas llenando un formulario. Puedes escribir o mandar un audio y explicar naturalmente qué ocurrió y cuál es tu relación con el inmueble.</p>

            <h3 className="mb-2 mt-8">02 — Envía lo que ya tienes</h3>
            <p>Contratos, pólizas, fotos, videos o soportes. Jovita extrae de esos archivos la información que ya existe para no volver a pedírtela.</p>

            <h3 className="mb-2 mt-8">03 — Jovita completa solo lo necesario</h3>
            <p>La conversación se adapta al caso. Pregunta únicamente por los vacíos que cambian la ruta o que impiden producir el siguiente documento o acción.</p>

            <h3 className="mb-2 mt-8">04 — Sales con algo accionable</h3>
            <p>Según el caso, Jovita puede preparar una comunicación al arrendador o inmobiliaria, organizar una reclamación de seguro, ayudarte a localizar una póliza asociada a un crédito o a una copropiedad, o dejar un expediente de evidencias y próximos pasos cuando no existe una cobertura identificada.</p>
          </div>

          <div className="mt-8">
            <a href={getWhatsAppUrl()} className="btn btn-accent" target="_blank" rel="noopener noreferrer">
              Probar Jovita en WhatsApp →
            </a>
          </div>
        </div>
      </section>

      {/* UX + Behavioral Science */}
      <section className="section">
        <div className="container">
          <h2>Menos carga cuando ya tienes demasiado encima</h2>
          <p>
            Un desastre ya consume atención, tiempo y capacidad de decisión. Por eso Jovita no obliga a navegar menús ni interrogatorios de sí/no: escucha un relato libre, usa lo que ya sabe y convierte la complejidad en pequeños pasos comprensibles.
          </p>
          <p>
            Diseñamos la conversación combinando IA y principios de ciencia del comportamiento para reducir carga cognitiva, fricción, repetición e incertidumbre. La interacción prioriza seguridad, empatía y claridad; en medio de una situación difícil, busca devolver algo de control: qué sabemos, qué falta y qué puedes hacer ahora.
          </p>
        </div>
      </section>

      {/* Por qué IA */}
      <section id="por-que-ia" className="section" style={{ backgroundColor: '#111', color: '#fff' }}>
        <div className="container">
          <span className="eyebrow" style={{ color: '#888' }}>Por qué IA</span>
          <h2 style={{ color: '#fff' }}>La IA no es una capa sobre el producto. Es el producto.</h2>
          <p style={{ color: '#eaeaea' }}>Jovita usa IA para:</p>
          
          <ul style={{ color: '#eaeaea' }}>
            <li>convertir lenguaje cotidiano en un caso estructurado;</li>
            <li>extraer información de contratos, pólizas, audios, imágenes y otros soportes;</li>
            <li>inferir la ruta probable sin obligar al usuario a clasificarse a sí mismo;</li>
            <li>decidir qué información falta y formular la siguiente pregunta útil;</li>
            <li>recuperar fuentes jurídicas y documentales relevantes para el caso;</li>
            <li>distinguir hechos reportados, evidencia disponible e información todavía no confirmada;</li>
            <li>generar documentos desde hechos confirmados, archivos del caso y fuentes recuperadas;</li>
            <li>retomar un caso más adelante sin hacer que la persona empiece de cero.</li>
          </ul>

          <p style={{ color: '#fff', fontWeight: 600, fontSize: '1.25rem', marginTop: '2rem' }}>
            La IA permite que el formulario desaparezca.
          </p>
          <p style={{ color: '#ccc' }}>
            El sistema mantiene por debajo una estructura precisa del caso, mientras el usuario mantiene una conversación natural.
          </p>
        </div>
      </section>

      {/* Casos que entiende */}
      <section className="section">
        <div className="container">
          <h2>Casos que entiende</h2>
          <p className="eyebrow" style={{ color: '#111', fontWeight: 500, letterSpacing: 'normal', textTransform: 'none', fontSize: '1rem' }}>
            Arrendamiento · Seguro privado · Crédito hipotecario · Propiedad horizontal · Cobertura no identificada
          </p>

          <div className="cases-grid">
            <div className="case-item">
              <h3>Arrendatario</h3>
              <p>Revisa contrato y evidencia para preparar una comunicación accionable al arrendador o a la inmobiliaria.</p>
            </div>
            
            <div className="case-item">
              <h3>Propietario con seguro</h3>
              <p>Lee la póliza, organiza hechos y evidencia y prepara el expediente y la comunicación o reclamación correspondiente a la etapa del caso.</p>
            </div>

            <div className="case-item">
              <h3>Propietario con crédito hipotecario</h3>
              <p>Si la persona cree que no tiene seguro pero todavía paga el crédito, Jovita puede abrir la ruta para localizar la póliza asociada al inmueble y retomar el caso cuando aparezca.</p>
            </div>

            <div className="case-item">
              <h3>Propiedad horizontal</h3>
              <p>Ayuda a verificar la póliza de la copropiedad y a distinguir entre daños en bienes comunes, privados o todavía inciertos.</p>
            </div>

            <div className="case-item">
              <h3>Sin cobertura identificada</h3>
              <p>No inventa una reclamación. Organiza la evidencia, explica qué se pudo verificar y deja siguientes pasos que puedan reutilizarse si después aparece una póliza u otra fuente de cobertura.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Confianza y límites */}
      <section className="section-small" style={{ borderTop: '1px solid rgba(0,0,0,0.05)', borderBottom: '1px solid rgba(0,0,0,0.05)' }}>
        <div className="container">
          <h3 style={{ fontSize: '1.125rem' }}>Confianza y límites</h3>
          <p style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>
            Jovita no diagnostica daño estructural, no certifica habitabilidad, no decide si una aseguradora debe indemnizar y no reemplaza a un abogado, ajustador, ingeniero o autoridad.
          </p>
          <p style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: 0 }}>
            Distingue entre lo que la persona reporta, lo que puede observarse en una evidencia y lo que requiere una verificación profesional. No rellena datos faltantes inventándolos y no fabrica una reclamación cuando no identifica una ruta válida.
          </p>
        </div>
      </section>

      {/* Bajo el capó */}
      <section className="section">
        <div className="container">
          <h2>Bajo el capó</h2>
          
          <div className="arch-block">
{`WhatsApp
   ↓
conversación + documentos + evidencia
   ↓
extracción multimodal
   ↓
estado estructurado y persistente del caso
   ↓
resolución de ruta + detección de vacíos críticos
   ↓
knowledge base jurídica / contractual
   ↓
documento accionable + anexos + siguientes pasos`}
          </div>

          <p>
            El árbol principal de rutas es pequeño y controlable. La IA trabaja donde aporta valor: comprender lenguaje natural y archivos, manejar incertidumbre, recuperar contexto relevante y generar outputs sustentados en los hechos y fuentes del caso.
          </p>

          <a href={GITHUB_URL} className="secondary-link mt-4" target="_blank" rel="noopener noreferrer">
            Ver arquitectura, código y README completo en GitHub →
          </a>
        </div>
      </section>

      {/* CTA Final */}
      <section className="section text-center" style={{ paddingBottom: '8rem' }}>
        <div className="container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h2 style={{ maxWidth: '800px', margin: '0 auto 2rem' }}>
            Un desastre ya es suficiente. El siguiente paso no debería sentirse imposible.
          </h2>
          
          <a href={getWhatsAppUrl()} className="btn btn-accent btn-large mb-8" target="_blank" rel="noopener noreferrer">
            Hablar con Jovita en WhatsApp
          </a>

          <div className="flex gap-4 justify-center" style={{ flexDirection: 'column', gap: '1rem' }}>
            <a href="#demo" className="secondary-link justify-center">Ver demo otra vez ↑</a>
            <a href={GITHUB_URL} className="secondary-link justify-center" target="_blank" rel="noopener noreferrer">Ver repositorio en GitHub ↗</a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          Jovita · CTW 2026
        </div>
      </footer>
    </>
  );
}
