export const WHATSAPP_NUMBER = "573000000000";
export const WHATSAPP_MESSAGE = "Hola, se dañó mi inmueble por un desastre. ¿Cómo me puedes ayudar?";
export const DEMO_VIDEO_SRC = "https://storage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"; // PLACEHOLDER VIDEO
export const DEMO_POSTER_SRC = ""; // PLACEHOLDER POSTER
export const GITHUB_URL = "https://github.com/PLACEHOLDER/PLACEHOLDER";

export function getWhatsAppUrl() {
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_MESSAGE)}`;
}
