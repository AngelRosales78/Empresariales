export default function Header() {
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
      <span className="header-note"><span aria-hidden="true" />Tu próxima buena historia</span>
    </header>
  )
}
