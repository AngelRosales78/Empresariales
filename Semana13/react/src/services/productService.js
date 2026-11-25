import apiClient from './apiClient'

const detailUrl = (id) => `products/${encodeURIComponent(id)}/`

// Images can only travel as multipart; a missing image keeps the stored one.
function toFormData(product) {
  const body = new FormData()
  Object.entries(product).forEach(([field, value]) => {
    if (value !== null && value !== undefined) body.append(field, value)
  })
  return body
}

export async function listProducts({ category, signal } = {}) {
  const params = category ? { category } : undefined
  const { data } = await apiClient.get('products/', { params, signal })
  return data
}

export async function getProduct(id, signal) {
  const { data } = await apiClient.get(detailUrl(id), { signal })
  return data
}

export async function createProduct(product) {
  const { data } = await apiClient.post('products/', toFormData(product))
  return data
}

export async function updateProduct(id, changes) {
  const { data } = await apiClient.patch(detailUrl(id), toFormData(changes))
  return data
}

export async function deleteProduct(id) {
  await apiClient.delete(detailUrl(id))
}
