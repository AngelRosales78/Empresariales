import Header from './components/Header.jsx'
import Hero from './components/Hero.jsx'
import MovieList from './components/MovieList.jsx'
import Footer from './components/Footer.jsx'
import { movies, featuredMovie } from './data/movies.js'

export default function App() {
  return (
    <div id="inicio">
      <a className="skip-link" href="#cartelera">Saltar a la cartelera</a>
      <Header />
      <main>
        <Hero movie={featuredMovie} />
        <MovieList movies={movies} />
        <aside className="cinema-note"><span className="note-symbol" aria-hidden="true">✳</span><p>Un buen plan no necesita mucho.<br /><strong>Una película. Tu gente. Y dejarse llevar.</strong></p><span className="note-tag">NOS VEMOS EN EL CINE ↗</span></aside>
      </main>
      <Footer />
    </div>
  )
}
