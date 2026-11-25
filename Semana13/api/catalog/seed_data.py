"""Fixed catalog data: (category, description, color, products).

Each product is (name, description, price, stock, shape).
"""

CATALOG = [
    ("Afiches", "Láminas impresas para decorar tu sala.", "#2f5d73", [
        ("Afiche Órbita", "Lámina A2 en papel mate de 200 g.", "39.90", 18, "poster"),
        ("Afiche Medianoche", "Lámina A3 con tinta de larga duración.", "29.90", 12, "poster"),
        ("Set de postales", "Diez postales ilustradas de la cartelera.", "19.50", 40, "cards"),
    ]),
    ("Ropa", "Prendas de algodón con diseños del cineclub.", "#a4503c", [
        ("Polo Cinéclub", "Polo unisex de algodón peinado.", "59.00", 25, "shirt"),
        ("Gorra Claqueta", "Gorra ajustable con bordado frontal.", "45.00", 0, "cap"),
        ("Bolsa de tela", "Bolsa resistente con asas largas.", "32.00", 30, "bag"),
    ]),
    ("Hogar", "Objetos para ver películas en casa.", "#4c6b3c", [
        ("Taza Función Doble", "Taza de cerámica de 350 ml.", "27.90", 22, "mug"),
        ("Balde de canchita", "Balde reutilizable de dos litros.", "24.90", 35, "bucket"),
        ("Cojín Butaca", "Cojín de 40 x 40 cm con funda lavable.", "54.90", 8, "cushion"),
    ]),
]
