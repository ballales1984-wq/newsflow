// Configurazione per backend locale
// Usa questo file quando vuoi testare con il backend sul PC locale
export const environment = {
  production: false,
  // Backend locale sul PC
  apiUrl: 'http://localhost:8000/api/v1'
  // Per ngrok, usa:
  // apiUrl: 'https://xxxx-xxxx-xxxx.ngrok-free.app/api/v1'
  // Per IP pubblico, usa:
  // apiUrl: 'http://[TUO_IP_PUBBLICO]:8000/api/v1'
};

