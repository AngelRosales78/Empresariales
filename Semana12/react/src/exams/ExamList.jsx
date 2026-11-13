import { useEffect, useState } from 'react'
import { deleteExam, describeError, listExams } from '../api/exams'

const dateFormat = new Intl.DateTimeFormat('es-PE', { dateStyle: 'medium', timeZone: 'America/Lima' })

export default function ExamList() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [deleteError, setDeleteError] = useState('')
  const [deleting, setDeleting] = useState(null)
  const [request, setRequest] = useState({ page: 1 })

  useEffect(() => {
    const controller = new AbortController()
    listExams(request.page, controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) setData(result)
      })
      .catch((failure) => {
        if (!controller.signal.aborted) setError(describeError(failure))
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false)
      })
    return () => controller.abort()
  }, [request])

  function load(page = request.page) {
    setError('')
    setDeleteError('')
    setLoading(true)
    setRequest({ page })
  }

  async function remove(exam) {
    if (!window.confirm(`¿Eliminar «${exam.title}» y sus preguntas?`)) return
    setDeleteError('')
    setDeleting(exam.id)
    try {
      await deleteExam(exam.id)
      load(data.results.length === 1 && request.page > 1 ? request.page - 1 : request.page)
    } catch (failure) {
      setDeleteError(describeError(failure))
    } finally {
      setDeleting(null)
    }
  }

  return (
    <>
      <header className="exam-heading">
        <div><h1>Exámenes</h1><p>Consulta y administra los exámenes del laboratorio.</p></div>
        <a className="exam-button" href="#nuevo">Nuevo examen</a>
      </header>
      {loading ? (
        <div className="exam-panel" aria-busy="true">
          <p role="status">Cargando exámenes…</p>
          {[1, 2, 3].map((row) => <div key={row} className="exam-skeleton" aria-hidden="true" />)}
        </div>
      ) : error ? (
        <div className="exam-panel">
          <p role="alert">{error}</p>
          <button className="exam-button" onClick={() => load()}>Reintentar</button>
        </div>
      ) : (
        <section className="exam-panel" aria-label="Listado de exámenes">
          <div className="exam-controls">
            <p>{data.count} {data.count === 1 ? 'examen' : 'exámenes'}</p>
            <button className="exam-secondary" disabled={deleting !== null} onClick={() => load()}>Actualizar</button>
          </div>
          {deleteError && <p role="alert">{deleteError}</p>}
          {data.results.length ? (
            <div className="exam-table-wrap">
              <table>
                <thead><tr><th scope="col">ID</th><th scope="col">Título</th><th scope="col">Preguntas</th><th scope="col">Fecha de alta</th><th scope="col">Acciones</th></tr></thead>
                <tbody>
                  {data.results.map((exam) => (
                    <tr key={exam.id}>
                      <td>{exam.id}</td><td>{exam.title}</td><td>{exam.question_count}</td>
                      <td>{dateFormat.format(new Date(exam.created_at))}</td>
                      <td><button className="exam-danger" disabled={deleting !== null} aria-label={`Eliminar ${exam.title}`} onClick={() => remove(exam)}>
                        {deleting === exam.id ? 'Eliminando…' : 'Eliminar'}
                      </button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : <p>Aún no hay exámenes registrados.</p>}
          {(data.previous || data.next) && (
            <nav className="exam-pagination" aria-label="Páginas del listado">
              <button className="exam-secondary" disabled={!data.previous || deleting !== null} onClick={() => load(request.page - 1)}>Anterior</button>
              <span>Página {request.page}</span>
              <button className="exam-secondary" disabled={!data.next || deleting !== null} onClick={() => load(request.page + 1)}>Siguiente</button>
            </nav>
          )}
        </section>
      )}
    </>
  )
}
