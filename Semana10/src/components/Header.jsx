export default function Header({ favoriteCount }) {
  return (
    <header className="site-header">
      <a className="brand" href="#inicio" aria-label="Cinéclub, inicio">
        <span className="brand-symbol" aria-hidden="true">c<span>✳</span></span>
        <span>cinéclub<span className="brand-dot">.</span></span>
      </a>
      <nav aria-label="Navegación principal">
        <a href="#cartelera">Cartelera</a>
        <a href="#destacada">La recomendada</a>
        <a href="#contacto">El cine</a>
      </nav>
      <a className="header-favorites" href="#cartelera" aria-label={`${favoriteCount} ${favoriteCount === 1 ? 'película favorita' : 'películas favoritas'}`}><span aria-hidden="true">♡</span> Tu colección <span>{favoriteCount}</span></a>
    </header>
  )
}
