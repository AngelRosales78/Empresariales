import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/',
  timeout: 8000,
  headers: {
    Accept: 'application/json',
    ...(import.meta.env.VITE_QUIZ_TOKEN && {
      Authorization: `Token ${import.meta.env.VITE_QUIZ_TOKEN}`,
    }),
  },
})

export async function listExams(page, signal) {
  const { data } = await client.get('exams/', { params: { page }, signal })
  return data
}

export async function createExam(body) {
  const { data } = await client.post('exams/', body)
  return data
}

export async function deleteExam(id) {
  await client.delete(`exams/${encodeURIComponent(id)}/`)
}

export function describeError(error) {
  if (!error.response) return 'No se pudo conectar con la API. Comprueba que Django esté en ejecución.'
  return error.response.data?.detail || `La API respondió con un error (${error.response.status}).`
}
