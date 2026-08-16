export const WHATSAPP_NUMBER = "573057152242";
export const WHATSAPP_MESSAGE = "Hola, se dañó mi inmueble por un desastre. ¿Cómo me puedes ayudar?";
export const YOUTUBE_VIDEO_ID = "XsVHu4hfu5E";
export const GITHUB_URL = "https://github.com/jrconstain/disaster-legal-assistant-ctw2026";

export function getWhatsAppUrl() {
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_MESSAGE)}`;
}
