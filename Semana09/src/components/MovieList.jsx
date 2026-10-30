import { useState } from 'react'
import MovieCard from './MovieCard.jsx'

export default function MovieList({ movies }) {
  const [genre, setGenre] = useState('Todas')
  const [search, setSearch] = useState('')
  const genres = ['Todas', ...new Set(movies.map((movie) => movie.genre))]
  const normalize = (text) => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
  const filteredMovies = movies.filter((movie) =>
    (genre === 'Todas' || movie.genre === genre) && normalize(movie.title).includes(normalize(search.trim())),
  )

  return (
    <section className="billboard" id="cartelera" aria-labelledby="billboard-title">
      <div className="section-heading">
        <div><p className="eyebrow">EL PLAN EMPIEZA AQUÍ</p><h2 id="billboard-title">Ahora en pantalla<span>.</span></h2></div>
        <p className="billboard-intro">Para desconectar del mundo.<br />Y conectar con una buena historia.</p>
      </div>
      <div className="billboard-toolbar">
        <div className="genre-filters" role="group" aria-label="Filtrar por género">
          {genres.map((item) => <button key={item} type="button" className={genre === item ? 'is-active' : ''}
            aria-pressed={genre === item} onClick={() => setGenre(item)}>{item}</button>)}
        </div>
        <label className="search-field"><span aria-hidden="true">⌕</span><span className="sr-only">Buscar película por título</span>
          <input type="search" placeholder="Busca tu próxima historia" value={search} onChange={(event) => setSearch(event.target.value)} />
        </label>
      </div>
      <div className="billboard-info"><p role="status">{filteredMovies.length} {filteredMovies.length === 1 ? 'película' : 'películas'} para descubrir</p><p><span className="live-dot" aria-hidden="true" /> CARTELERA DE DEMOSTRACIÓN</p></div>
      <div className="movie-grid">
        {filteredMovies.map((movie) => <MovieCard key={movie.id} movie={movie} />)}
      </div>
      {filteredMovies.length === 0 && <div className="empty-state"><h3>Esa historia todavía no está aquí.</h3><p>Prueba con otro título o explora toda la cartelera.</p><button type="button" onClick={() => { setSearch(''); setGenre('Todas') }}>Ver todas las películas ↗</button></div>}
    </section>
  )
}
