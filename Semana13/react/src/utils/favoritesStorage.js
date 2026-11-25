export const FAVORITES_KEY = 'cineclub:semana10:favorites:v1'

export function readFavorites(validIds) {
  try {
    const stored = JSON.parse(window.localStorage.getItem(FAVORITES_KEY) ?? '[]')
    if (!Array.isArray(stored)) return []
    return [...new Set(stored.filter((id) => typeof id === 'string' && validIds.includes(id)))]
  } catch (error) {
    console.warn('No se pudieron recuperar las favoritas; se inicia una lista vacía.', error.name)
    return []
  }
}

export function saveFavorites(ids) {
  try {
    window.localStorage.setItem(FAVORITES_KEY, JSON.stringify(ids))
    return true
  } catch (error) {
    console.warn('No se pudieron guardar las favoritas en este navegador.', error.name)
    return false
  }
}
