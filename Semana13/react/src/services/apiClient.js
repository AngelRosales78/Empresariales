import axios from 'axios'

// The only place that knows the API address and credentials.
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/',
  timeout: 8000,
  headers: {
    Accept: 'application/json',
    ...(import.meta.env.VITE_QUIZ_TOKEN && {
      Authorization: `Token ${import.meta.env.VITE_QUIZ_TOKEN}`,
    }),
  },
})

export function describeError(error) {
  if (!error.response) return 'No se pudo conectar con la API. Comprueba que Django esté en ejecución.'
  return error.response.data?.detail || `La API respondió con un error (${error.response.status}).`
}

export function getFieldErrors(error) {
  const data = error.response?.status === 400 ? error.response.data : null
  if (!data || typeof data !== 'object') return {}
  return Object.fromEntries(Object.entries(data)
    .filter(([, messages]) => Array.isArray(messages))
    .map(([field, messages]) => [field, messages.join(' ')]))
}

export default apiClient
