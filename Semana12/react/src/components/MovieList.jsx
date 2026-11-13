import { useEffect, useMemo, useState } from 'react'
import MovieCard from './MovieCard.jsx'
import Button from './Button.jsx'

const normalize = (text) => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()

export default function MovieList({ movies, searchText, favoriteIds, onToggleFavorite, onClearSearch, isPending }) {
  const [genre, setGenre] = useState('Todas')
  const [onlyFavorites, setOnlyFavorites] = useState(false)
  const genres = ['Todas', ...new Set(movies.map((movie) => movie.genre))]

  // The raw input is not a dependency: typing does not recalculate the filter.
  const filteredMovies = useMemo(() => movies.filter((movie) =>
    (genre === 'Todas' || movie.genre === genre) &&
    (!onlyFavorites || favoriteIds.includes(movie.id)) &&
    normalize(movie.title).includes(normalize(searchText.trim())),
  ), [movies, searchText, genre, onlyFavorites, favoriteIds])

  useEffect(() => {
    if (import.meta.env.DEV) console.info('[filtro ejecutado]', JSON.stringify({ texto: searchText, genero: genre, soloFavoritas: onlyFavorites, resultados: filteredMovies.length }))
  }, [filteredMovies, searchText, genre, onlyFavorites])

  function resetFilters() {
    setGenre('Todas')
    setOnlyFavorites(false)
    onClearSearch()
  }

  return (
    <section className="billboard" id="cartelera" aria-labelledby="billboard-title" aria-busy={isPending}>
      <div className="section-heading">
        <div><p className="eyebrow">EL PLAN EMPIEZA AQUÍ</p><h2 id="billboard-title">Ahora en pantalla<span>.</span></h2></div>
        <p className="billboard-intro">Encuentra la tuya.<br />Guarda las que no quieres perderte.</p>
      </div>
      <div className="billboard-toolbar">
        <div className="genre-filters" role="group" aria-label="Filtrar por género">
          {genres.map((item) => <Button key={item} variant="chip" className={genre === item ? 'is-active' : ''}
            aria-pressed={genre === item} onClick={() => setGenre(item)}>{item}</Button>)}
        </div>
        <Button variant="secondary" className="favorites-filter" aria-pressed={onlyFavorites} onClick={() => setOnlyFavorites((current) => !current)}>
          <span aria-hidden="true">{onlyFavorites ? '♥' : '♡'}</span> Mis favoritas <span className="favorite-count">{favoriteIds.length}</span>
        </Button>
      </div>
      <div className="billboard-info">
        <p role="status">{isPending ? 'Actualizando resultados…' : `${filteredMovies.length} ${filteredMovies.length === 1 ? 'película' : 'películas'} para descubrir`}{searchText.trim() && !isPending ? ` · «${searchText.trim()}»` : ''}</p>
        <p><span className="live-dot" aria-hidden="true" /> CARTELERA DE DEMOSTRACIÓN</p>
      </div>
      <div className="movie-grid">
        {filteredMovies.map((movie) => <MovieCard key={movie.id} movie={movie}
          isFavorite={favoriteIds.includes(movie.id)} onToggleFavorite={onToggleFavorite} />)}
      </div>
      {filteredMovies.length === 0 && !isPending && (
        <div className="empty-state">
          <span className="empty-symbol" aria-hidden="true">⌕</span>
          <p className="eyebrow">SIGAMOS BUSCANDO</p>
          <h3>{onlyFavorites && !searchText.trim() ? 'Tu próxima favorita te está esperando.' : 'Esa historia todavía no está aquí.'}</h3>
          <p>{searchText.trim() ? <>No encontramos películas para <strong>«{searchText.trim()}»</strong> con estos filtros.</> : 'No hay películas que coincidan con los filtros seleccionados.'}</p>
          <p>Prueba otro título o vuelve a descubrir toda la cartelera.</p>
          <Button variant="primary" onClick={resetFilters}>Ver todas las películas <span aria-hidden="true">↗</span></Button>
        </div>
      )}
    </section>
  )
}
