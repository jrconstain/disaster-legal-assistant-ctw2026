import { useState, useEffect } from 'react';
import NavBar from './components/NavBar';
import Landing from './pages/Landing';
import Team from './pages/Team';
import DataPolicy from './pages/DataPolicy';

export default function App() {
  const [hash, setHash] = useState(window.location.hash);

  useEffect(() => {
    const onHashChange = () => {
      const newHash = window.location.hash;
      setHash(newHash);
      
      if (newHash === '#equipo' || newHash === '#politica') {
        window.scrollTo(0, 0);
      } else {
        // Rutas de la landing page
        if (newHash === '' || newHash === '#') {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
          // Pequeño timeout para permitir que React renderice Landing primero si venimos de otra página
          setTimeout(() => {
            const id = newHash.replace('#', '');
            const element = document.getElementById(id);
            if (element) {
              element.scrollIntoView({ behavior: 'smooth' });
            }
          }, 50);
        }
      }
    };
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  let content;
  if (hash === '#equipo') {
    content = <Team />;
  } else if (hash === '#politica') {
    content = <DataPolicy />;
  } else {
    // Para rutas vacías, '/', o enlaces como '#demo' que son anclas en Landing
    content = <Landing />;
  }

  return (
    <>
      <NavBar />
      
      {content}

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', marginBottom: '1.5rem' }}>
            <a href="#equipo" className="secondary-link">Equipo</a>
            <a href="#politica" className="secondary-link">Política de Datos y Uso</a>
          </div>
          <div>Jovita · CTW 2026</div>
        </div>
      </footer>
    </>
  );
}
