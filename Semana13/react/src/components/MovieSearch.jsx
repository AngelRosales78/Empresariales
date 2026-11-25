import { useId } from 'react'
import Button from './Button.jsx'

export default function MovieSearch({ value, onChange, onSubmit, isPending }) {
  const inputId = useId()

  return (
    <form className="movie-search" role="search" onSubmit={(event) => { event.preventDefault(); onSubmit() }}>
      <label className="search-label" htmlFor={inputId}>Encuentra tu próxima historia</label>
      <div className="search-controls">
        <div className="search-input-wrap">
          <span className="search-icon" aria-hidden="true">⌕</span>
          <input id={inputId} type="search" value={value} placeholder="Título de la película…"
            autoComplete="off" onChange={(event) => onChange(event.target.value)}
            aria-describedby={`${inputId}-hint`} />
          {value && <Button variant="icon" className="clear-search" aria-label="Limpiar búsqueda" onClick={() => onChange('')}>×</Button>}
        </div>
        <Button variant="primary" type="submit">Buscar <span aria-hidden="true">↗</span></Button>
      </div>
      <p className="search-hint" id={`${inputId}-hint`} role="status">
        {isPending ? 'Buscando tu próxima película…' : 'Ocho historias. Una para ti. Busca por título.'}
      </p>
    </form>
  )
}
