// Serviço para gerenciar carregamento de imagens com fallback

export const getImageUrl = (originalUrl: string | undefined): string => {
  if (!originalUrl) {
    return 'https://via.placeholder.com/500x500/e5e7eb/9ca3af?text=Sem+Imagem';
  }

  // Tenta a URL original primeiro
  // Se falhar, retorna uma URL placeholder
  return originalUrl;
};

export const getProxiedImageUrl = (originalUrl: string | undefined): string => {
  if (!originalUrl) {
    return 'https://via.placeholder.com/500x500/e5e7eb/9ca3af?text=Sem+Imagem';
  }

  const API_URL = 'http://localhost:8000/images/proxy';
  return `${API_URL}?url=${encodeURIComponent(originalUrl)}`;
};

// Retorna a melhor URL de imagem disponível
export const getBestImageUrl = (
  originalUrl: string | undefined,
  useProxy: boolean = false
): string => {
  if (!originalUrl) {
    return 'https://via.placeholder.com/500x500/e5e7eb/9ca3af?text=Sem+Imagem';
  }

  // Se for URL do Wikimedia, tentar diretamente (geralmente tem CORS)
  if (originalUrl.includes('wikimedia.org')) {
    return originalUrl;
  }

  // Para outras URLs, usar proxy se necessário
  if (useProxy) {
    return getProxiedImageUrl(originalUrl);
  }

  return originalUrl;
};
