import { useEffect, useRef, useState } from 'react';
import { DEMO_VIDEO_SRC, DEMO_POSTER_SRC, getWhatsAppUrl } from '../config';

export default function DemoHero() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isBlocked, setIsBlocked] = useState(false);
  const [isEnded, setIsEnded] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    // We intentionally try to play with sound as requested
    video.muted = false;
    const playPromise = video.play();

    if (playPromise !== undefined) {
      playPromise.catch((error) => {
        console.log("Autoplay with sound blocked by browser:", error);
        setIsBlocked(true);
        // Requirement: Do NOT automatically switch to muted. Show button.
      });
    }
  }, []);

  const handleForcePlay = () => {
    if (videoRef.current) {
      videoRef.current.muted = false;
      videoRef.current.play();
      setIsBlocked(false);
      setIsEnded(false);
    }
  };

  const handleEnded = () => {
    setIsEnded(true);
  };

  const handleReplay = (e: React.MouseEvent) => {
    e.preventDefault();
    if (videoRef.current) {
      videoRef.current.currentTime = 0;
      handleForcePlay();
    }
  };

  return (
    <section id="demo" className="section pb-0" style={{ paddingTop: '2rem' }}>
      <div className="container">
        <div className="video-wrapper" id="demo-video-wrapper" style={{ marginBottom: '3rem' }}>
          <video
            ref={videoRef}
            src={DEMO_VIDEO_SRC}
            poster={DEMO_POSTER_SRC}
            playsInline
            controls={!isBlocked && !isEnded}
            preload="auto"
            onEnded={handleEnded}
            className={`main-video ${isEnded ? 'dimmed' : ''}`}
          />

          {isBlocked && (
            <div className="video-overlay" style={{ background: 'rgba(0,0,0,0.6)' }}>
              <button onClick={handleForcePlay} className="btn btn-large">
                Reproducir demo con sonido
              </button>
            </div>
          )}

          {isEnded && (
            <div className="video-overlay ended-overlay">
              <h3>¿Te pasó algo parecido?</h3>
              <a href={getWhatsAppUrl()} className="btn btn-accent btn-large" target="_blank" rel="noopener noreferrer">
                Hablar con Jovita en WhatsApp →
              </a>
              <button onClick={handleReplay} className="link-btn mt-4">
                Ver demo otra vez
              </button>
            </div>
          )}
        </div>

        <div className="hero-content">
          <h1>Tu inmueble fue afectado por un desastre. Jovita te ayuda a saber qué sigue.</h1>
          <p>Habla como hablas. Envía contratos, pólizas, audios y fotos. Jovita organiza tu caso y convierte esa conversación en un siguiente paso accionable.</p>
          <a href={getWhatsAppUrl()} className="btn btn-accent" target="_blank" rel="noopener noreferrer">
            Hablar con Jovita en WhatsApp
          </a>
        </div>
      </div>
    </section>
  );
}
