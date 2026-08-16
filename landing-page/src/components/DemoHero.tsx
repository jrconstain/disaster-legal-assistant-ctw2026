import { useEffect, useRef, useState } from 'react';
import { getWhatsAppUrl, YOUTUBE_VIDEO_ID } from '../config';

export default function DemoHero() {
  const playerRef = useRef<any>(null);
  const [isEnded, setIsEnded] = useState(false);

  useEffect(() => {
    let player: any;

    const initPlayer = () => {
      // @ts-ignore
      player = new window.YT.Player('youtube-player', {
        videoId: YOUTUBE_VIDEO_ID,
        playerVars: {
          autoplay: 1, // Intentar autoplay (YouTube maneja la restricción del navegador)
          controls: 1,
          rel: 0,
          modestbranding: 1,
          playsinline: 1
        },
        events: {
          onStateChange: (event: any) => {
            // @ts-ignore
            if (event.data === window.YT.PlayerState.ENDED) {
              setIsEnded(true);
            }
            // @ts-ignore
            if (event.data === window.YT.PlayerState.PLAYING) {
              setIsEnded(false);
            }
          }
        }
      });
      playerRef.current = player;
    };

    // @ts-ignore
    if (!window.YT) {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag?.parentNode?.insertBefore(tag, firstScriptTag);
      // @ts-ignore
      window.onYouTubeIframeAPIReady = initPlayer;
    } else {
      initPlayer();
    }

    return () => {
      if (playerRef.current && typeof playerRef.current.destroy === 'function') {
        playerRef.current.destroy();
      }
    };
  }, []);

  const handleReplay = (e: React.MouseEvent) => {
    e.preventDefault();
    if (playerRef.current && typeof playerRef.current.seekTo === 'function') {
      playerRef.current.seekTo(0);
      playerRef.current.playVideo();
      setIsEnded(false);
    }
  };

  return (
    <section id="demo" className="section pb-0" style={{ paddingTop: '2rem' }}>
      <div className="container">
        <div className="video-wrapper" id="demo-video-wrapper" style={{ marginBottom: '3rem' }}>
          
          <div id="youtube-player" className={`main-video ${isEnded ? 'dimmed' : ''}`}></div>

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
