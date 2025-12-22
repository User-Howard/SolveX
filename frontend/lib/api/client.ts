const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const baseUrl = API_BASE_URL.endsWith('/')
    ? API_BASE_URL.slice(0, -1)
    : API_BASE_URL;
  const response = await fetch(`${baseUrl}${normalizedEndpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'API request failed' }));
    throw new Error(error.detail || 'API request failed');
  }

  return response.json();
}
