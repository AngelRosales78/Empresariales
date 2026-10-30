import { useState } from 'react'
import Button from './Button.jsx'

export default function MovieCard({ movie, isFavorite, onToggleFavorite }) {
  const [selectedTime, setSelectedTime] = useState(null)

  return (
    <article className="movie-card" id={`pelicula-${movie.id}`} aria-labelledby={`title-${movie.id}`}>
      <div className="movie-poster">
        <img src={movie.image} alt={`Afiche ilustrado de ${movie.title}`} loading="lazy" width="400" height="600" />
        <span className="poster-classification" aria-label={`Clasificación: ${movie.classification}`}>{movie.classification}</span>
        {movie.featured && <span className="poster-featured">NUESTRA ELECCIÓN</span>}
        <Button variant="favorite" className="favorite-toggle" aria-pressed={isFavorite}
          aria-label={`${isFavorite ? 'Quitar' : 'Agregar'} ${movie.title} ${isFavorite ? 'de' : 'a'} favoritas`}
          onClick={() => onToggleFavorite(movie.id)}>
          <span aria-hidden="true">{isFavorite ? '♥' : '♡'}</span>
        </Button>
      </div>
      <div className="movie-heading">
        <h3 id={`title-${movie.id}`}>{movie.title}</h3>
        <span className="movie-rating" aria-label={`Valoración: ${movie.rating} de 10`}><span aria-hidden="true">★</span> {movie.rating.toFixed(1)}</span>
      </div>
      <p className="movie-meta">{movie.genre}<span aria-hidden="true">·</span>{movie.duration} min</p>
      <p className="movie-synopsis">{movie.synopsis}</p>
      <p className="showtimes-label">FUNCIONES DE HOY</p>
      <div className="showtimes" aria-label={`Horarios de ${movie.title}`}>
        {movie.showtimes.map((time) => (
          <Button key={time} variant="time" aria-pressed={selectedTime === time}
            aria-label={`${movie.title}, función ${time}`}
            onClick={() => setSelectedTime(selectedTime === time ? null : time)}>{time}</Button>
        ))}
      </div>
      <p className="selection-note" role="status">{selectedTime ? `${selectedTime} seleccionada · Función de demostración` : '\u00a0'}</p>
    </article>
  )
}
