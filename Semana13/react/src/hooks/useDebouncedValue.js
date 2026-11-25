import { useEffect, useState } from 'react'

export default function useDebouncedValue(value, delay = 400) {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    // Cancels the previous timer when another character arrives or on unmount.
    const timeout = window.setTimeout(() => {
      setDebouncedValue(value)
      if (import.meta.env.DEV) console.info('[búsqueda aplicada]', value)
    }, delay)
    return () => window.clearTimeout(timeout)
  }, [value, delay])

  return debouncedValue
}
