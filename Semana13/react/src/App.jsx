import { useEffect, useState } from 'react'
import Header from './components/Header.jsx'
import Hero from './components/Hero.jsx'
import MovieList from './components/MovieList.jsx'
import Footer from './components/Footer.jsx'
import useDebouncedValue from './hooks/useDebouncedValue.js'
import { readFavorites, saveFavorites } from './utils/favoritesStorage.js'
import { movies, featuredMovie } from './data/movies.js'

const movieIds = movies.map((movie) => movie.id)

export default function App() {
  const [favoriteIds, setFavoriteIds] = useState(() => readFavorites(movieIds))
  const [searchText, setSearchText] = useState('')
  const [storageUnavailable, setStorageUnavailable] = useState(false)
  const debouncedSearch = useDebouncedValue(searchText, 400)

  useEffect(() => {
    setStorageUnavailable(!saveFavorites(favoriteIds))
  }, [favoriteIds])

  function toggleFavorite(movieId) {
    if (!movieIds.includes(movieId)) return
    setFavoriteIds((current) => current.includes(movieId)
      ? current.filter((id) => id !== movieId)
      : [...current, movieId])
  }

  function updateSearch(value) {
    setSearchText(value)
    if (import.meta.env.DEV) console.info('[entrada inmediata]', value)
  }

  function goToMovies() {
    document.getElementById('cartelera')?.scrollIntoView({ block: 'start' })
  }

  return (
    <div id="inicio">
      <a className="skip-link" href="#cartelera">Saltar a la cartelera</a>
      <Header favoriteCount={favoriteIds.length} />
      <main>
        <Hero movie={featuredMovie} searchText={searchText} onSearchChange={updateSearch}
          onSearchSubmit={goToMovies} isPending={searchText !== debouncedSearch} />
        {storageUnavailable && <p className="storage-notice" role="alert">Puedes marcar favoritas, pero este navegador no permite guardarlas para la próxima visita.</p>}
        <MovieList movies={movies} searchText={debouncedSearch} favoriteIds={favoriteIds}
          onToggleFavorite={toggleFavorite} onClearSearch={() => updateSearch('')}
          isPending={searchText !== debouncedSearch} />
        <aside className="cinema-note"><span className="note-symbol" aria-hidden="true">✳</span><p>Algunas historias merecen volver a verse.<br /><strong>Guarda tus favoritas. Encuentra tu próximo gran plan.</strong></p><span className="note-tag">TU CINE, A TU MANERA ↗</span></aside>
      </main>
      <Footer />
    </div>
  )
}
