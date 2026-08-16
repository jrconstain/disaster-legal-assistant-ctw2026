import React from 'react';

export default function Team() {
  return (
    <section className="section" style={{ minHeight: '80vh', paddingTop: '4rem' }}>
      <div className="container">
        <h1>El Equipo</h1>
        <span className="eyebrow">Hackathon CTW 2026</span>

        <p style={{ marginTop: '2rem' }}>
          Somos un equipo multidisciplinario enfocado en crear soluciones en la intersección de la IA y el impacto real.
        </p>

        <div className="team-grid">
          <div className="team-card">
            <img src="/juan.jpeg" alt="Juan José Rojas" className="team-avatar" />
            <h3>Juan José Rojas</h3>
            <p style={{ margin: 0, fontSize: '1rem' }}>Científico del comportamiento y economista, obsesionado con los LLMs y la reducción de carga cognitiva.</p>
          </div>

          <div className="team-card">
            <img src="/rafael.jpeg" alt="Rafael Angulo" className="team-avatar" />
            <h3>Rafael Angulo</h3>
            <p style={{ margin: 0, fontSize: '1rem' }}>Ingeniero de software experto en chatbots y JavaScript. El arquitecto detrás de la experiencia de mensajería.</p>
          </div>

          <div className="team-card">
            <img src="/gustavo.jpeg" alt="Gustavo Cedeño" className="team-avatar" />
            <h3>Gustavo Cedeño</h3>
            <p style={{ margin: 0, fontSize: '1rem' }}>Economista especialista en datos, enfocado en estructurar la información y conectar los puntos lógicos.</p>
          </div>

          <div className="team-card">
            <img src="/carlos.jpeg" alt="Carlos Caicedo" className="team-avatar" />
            <h3>Carlos Caicedo</h3>
            <p style={{ margin: 0, fontSize: '1rem' }}>Estudiante de ingeniería biomédica, aportando precisión estructural y metodológica al proyecto.</p>
          </div>
        </div>

        <h3 className="mb-4 mt-8 pt-8" style={{ borderTop: '1px solid rgba(0,0,0,0.05)' }}>
          Detrás de cámaras
        </h3>

        <div className="photo-grid">
          <img src="/foto1.jpg" alt="Equipo en la hackathon" />
          <img src="/foto2.jpg" alt="Trabajando en el código" />
          <img src="/foto3.jpg" alt="Estatua en la plaza" />
          <img src="/foto4.jpg" alt="Desarrollo del proyecto" />
        </div>
      </div>
    </section>
  );
}
