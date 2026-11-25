import apiClient from './apiClient'

const detailUrl = (id) => `categories/${encodeURIComponent(id)}/`

export async function listCategories(signal) {
  const { data } = await apiClient.get('categories/', { signal })
  return data
}

export async function getCategory(id, signal) {
  const { data } = await apiClient.get(detailUrl(id), { signal })
  return data
}

export async function createCategory(category) {
  const { data } = await apiClient.post('categories/', category)
  return data
}

export async function updateCategory(id, changes) {
  const { data } = await apiClient.patch(detailUrl(id), changes)
  return data
}

export async function deleteCategory(id) {
  await apiClient.delete(detailUrl(id))
}
