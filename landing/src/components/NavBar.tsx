import { getWhatsAppUrl, GITHUB_URL } from '../config';

export default function NavBar() {
  return (
    <nav className="navbar">
      <div className="container nav-container">
        <a href="#" className="logo" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <img src="/logo.jpeg" alt="Logo Jovita" style={{ width: '32px', height: '32px', borderRadius: '50%', mixBlendMode: 'multiply', objectFit: 'cover' }} />
          <span>Jovita.</span>
        </a>
        
        <div className="nav-links">
          <a href="#" className="nav-link">Inicio</a>
          <a href="#demo" className="nav-link">Demo</a>
          <a href="#como-funciona" className="nav-link">Cómo funciona</a>
          <a href="#por-que-ia" className="nav-link">Por qué IA</a>
          
          <div className="nav-dropdown">
            <span className="nav-link" style={{cursor: 'pointer'}}>Más ▾</span>
            <div className="dropdown-content">
              <a href="#equipo" className="dropdown-item">Equipo</a>
              <a href="#politica" className="dropdown-item">Política de datos</a>
            </div>
          </div>

          <a href={GITHUB_URL} className="nav-link" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>

        <div>
          <a href={getWhatsAppUrl()} className="btn" target="_blank" rel="noopener noreferrer">
            Hablar con Jovita
          </a>
        </div>
      </div>
    </nav>
  );
}
