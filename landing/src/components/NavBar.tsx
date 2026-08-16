import { getWhatsAppUrl, GITHUB_URL } from '../config';

export default function NavBar() {
  return (
    <nav className="navbar">
      <div className="container nav-container">
        <a href="#" className="logo">Jovita.</a>
        
        <div className="nav-links">
          <a href="#demo" className="nav-link">Demo</a>
          <a href="#como-funciona" className="nav-link">Cómo funciona</a>
          <a href="#por-que-ia" className="nav-link">Por qué IA</a>
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
