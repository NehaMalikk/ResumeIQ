import { createApiError } from '@/services/apiErrors'
import type { AnalyzeResponse } from '@/types'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '/api').replace(/\/+$/, '')

export async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const headers = new Headers(options?.headers)
  if (options?.body && !(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  const response = await fetch(`${API_BASE_URL}/${endpoint.replace(/^\/+/, '')}`, {
    ...options,
    headers,
  })
  if (!response.ok) throw await createApiError(response)
  return response.json() as Promise<T>
}

export const api = {
  analyzeResume(resume: File, jobDescription: string, signal?: AbortSignal) {
    const formData = new FormData()
    formData.append('resume', resume)
    formData.append('job_description', jobDescription.trim())
    return apiFetch<AnalyzeResponse>('/analyze', {
      method: 'POST',
      body: formData,
      signal,
    })
  },
}
