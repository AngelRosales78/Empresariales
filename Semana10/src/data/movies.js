// Cartelera ficticia creada para el laboratorio. No representa funciones reales.
export const movies = [
  {
    id: 'orbita', title: 'Órbita', image: '/images/orbita.svg',
    banner: '/images/orbita-banner.svg', genre: 'Ciencia ficción',
    synopsis: 'En el silencio de un planeta lejano, una astronauta descubre que el viaje más importante no siempre nos lleva más lejos, sino de vuelta a nosotros mismos.',
    classification: '+12', rating: 8.7, duration: 142,
    showtimes: ['15:30', '18:15', '21:00'], featured: true,
  },
  {
    id: 'ultima-luz', title: 'La última luz', image: '/images/ultima-luz.svg',
    genre: 'Drama', synopsis: 'Una fotógrafa regresa a las montañas de su infancia para cumplir una promesa y encuentra una historia que todavía espera ser contada.',
    classification: '+12', rating: 8.4, duration: 118,
    showtimes: ['14:00', '17:00', '20:00'],
  },
  {
    id: 'casa-mar', title: 'La casa del mar', image: '/images/casa-mar.svg',
    genre: 'Drama', synopsis: 'Dos hermanos heredan una casa frente al océano. Entre recuerdos y mareas, deberán decidir qué significa realmente volver a casa.',
    classification: 'APT', rating: 8.2, duration: 106,
    showtimes: ['14:30', '17:15', '19:45'],
  },
  {
    id: 'medianoche', title: 'Medianoche', image: '/images/medianoche.svg',
    genre: 'Suspenso', synopsis: 'Una llamada equivocada lleva a un músico a recorrer una ciudad que oculta sus secretos bajo la lluvia. Tiene una noche para encontrar la verdad.',
    classification: '+16', rating: 8.6, duration: 124,
    showtimes: ['16:00', '19:00', '21:45'],
  },
  {
    id: 'jardin', title: 'El jardín secreto', image: '/images/jardin.svg',
    genre: 'Fantasía', synopsis: 'Una joven encuentra una puerta entre las plantas del patio. Detrás crece un jardín que solo florece cuando alguien se atreve a compartir un recuerdo.',
    classification: 'APT', rating: 8.1, duration: 102,
    showtimes: ['13:00', '15:30', '18:00'],
  },
  {
    id: 'kilometro', title: 'Kilómetro cero', image: '/images/kilometro.svg',
    genre: 'Aventura', synopsis: 'Tres desconocidos, un auto prestado y una ruta sin señal. Lo que comienza como un desvío se convierte en el viaje que todos necesitaban.',
    classification: '+12', rating: 7.9, duration: 112,
    showtimes: ['14:15', '17:30', '20:15'],
  },
  {
    id: 'pequenos', title: 'Pequeños gigantes', image: '/images/pequenos.svg',
    genre: 'Animación', synopsis: 'Un oso tímido y una pequeña coneja cruzan el bosque para devolver una estrella al cielo. Descubrirán que el valor no se mide en centímetros.',
    classification: 'APT', rating: 8.5, duration: 94,
    showtimes: ['12:00', '14:30', '16:45'],
  },
  {
    id: 'entre-notas', title: 'Entre notas', image: '/images/entre-notas.svg',
    genre: 'Romance', synopsis: 'Una pianista y un compositor comparten una sala de ensayo por accidente. Con cada melodía, sus mundos comienzan a encontrar el mismo ritmo.',
    classification: '+12', rating: 8.3, duration: 116,
    showtimes: ['15:00', '18:00', '20:45'],
  },
]

export const featuredMovie = movies.find((movie) => movie.featured)
