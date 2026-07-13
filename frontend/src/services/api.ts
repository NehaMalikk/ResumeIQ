const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

/**
 * Base fetch wrapper — ready for backend integration.
 * Replace mock data calls with these methods when API is available.
 */
export async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`)
  }

  return response.json() as Promise<T>
}

export const api = {
  analyzeResume: (formData: FormData) =>
    apiFetch('/analyze', { method: 'POST', body: formData }),
  getDemoAnalysis: () => apiFetch('/demo'),
}
