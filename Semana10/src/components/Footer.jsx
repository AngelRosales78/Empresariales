export default function Footer() {
  return (
    <footer className="site-footer" id="contacto">
      <div className="footer-top">
        <div className="footer-brand"><a className="brand" href="#inicio">cinéclub<span className="brand-dot">.</span></a><p>Las mejores historias<br />se viven en pantalla grande.</p></div>
        <div><h2>Hablemos de cine</h2><a href="mailto:hola@cineclub.example">hola@cineclub.example</a><p>Contacto ilustrativo del proyecto</p></div>
        <div><h2>Una sala para todos</h2><p>APT · Todo público<br />+12 · Mayores de 12 años<br />+16 · Mayores de 16 años</p></div>
        <a className="back-top" href="#inicio" aria-label="Volver al inicio">↑</a>
      </div>
      <div className="footer-bottom"><p>© {new Date().getFullYear()} Cinéclub. Hecho para quienes aman el cine.</p><p>Proyecto académico · Películas, valoraciones y funciones ficticias.</p></div>
    </footer>
  )
}
