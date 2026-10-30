import { writeFileSync } from 'node:fs'

// Solo modifica el ejemplo aislado; nunca toca App.jsx ni sus componentes.
const examples = {
  class: 'export default function Example() { return <div class="demo">Error deliberado: class en vez de className</div> }\n',
  roots: 'export default function Example() { return (\n  <h1>Primer nodo</h1>\n  <p>Segundo nodo sin fragmento</p>\n) }\n',
  key: 'export default function Example() { return <ul>{["Órbita", "Medianoche"].map((title) => <li>{title}</li>)}</ul> }\n',
  reset: 'export default function Example() { return <main><h1>Laboratorio restaurado</h1><p>Los tres errores están documentados. La aplicación principal funciona sin ellos.</p><a href="/">Volver a Cinéclub</a></main> }\n',
}
const mode = process.argv[2]
if (!Object.hasOwn(examples, mode)) {
  console.error('Uso: node scripts/error-demo.mjs class|roots|key|reset')
  process.exit(1)
}
writeFileSync(new URL('../experiments/Example.jsx', import.meta.url), examples[mode], 'utf8')
console.log(`Ejemplo ${mode} preparado. Abre /laboratorio-errores.html y revisa la consola del navegador.`)
