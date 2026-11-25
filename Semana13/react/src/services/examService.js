import apiClient from './apiClient'

export async function listExams(page, signal) {
  const { data } = await apiClient.get('exams/', { params: { page }, signal })
  return data
}

export async function createExam(body) {
  const { data } = await apiClient.post('exams/', body)
  return data
}

export async function deleteExam(id) {
  await apiClient.delete(`exams/${encodeURIComponent(id)}/`)
}
