import MovieSearch from './MovieSearch.jsx'

export default function Hero({ movie, searchText, onSearchChange, onSearchSubmit, isPending }) {
  return (
    <section className="hero" id="destacada" aria-labelledby="featured-title">
      <img className="hero-art" src={movie.banner} alt="Paisaje de un planeta lejano bajo un gigante con anillos" fetchPriority="high" />
      <div className="hero-shade" />
      <div className="hero-copy">
        <p className="eyebrow"><span className="tiny-star" aria-hidden="true">✳</span> LA ELECCIÓN DE LA SEMANA</p>
        <p className="hero-kicker">Hay historias que te llevan más lejos.</p>
        <h1 id="featured-title">{movie.title}<span>.</span></h1>
        <div className="film-meta">
          <span>{movie.genre}</span><span>{movie.duration} min</span><span className="classification">{movie.classification}</span>
        </div>
        <p className="hero-synopsis">{movie.synopsis}</p>
        <MovieSearch value={searchText} onChange={onSearchChange} onSubmit={onSearchSubmit} isPending={isPending} />
      </div>
      <div className="hero-caption"><span>01 / 08</span><span>EN PANTALLA, EN OTRO MUNDO.</span></div>
      <span className="hero-vertical" aria-hidden="true">UNA PELÍCULA. MIL FORMAS DE SENTIR.</span>
    </section>
  )
}
