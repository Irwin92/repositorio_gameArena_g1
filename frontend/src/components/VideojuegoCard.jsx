export default function VideojuegoCard({ videojuego }) {
    return (
        <article>
            <h3>{videojuego.nombre}</h3>
            <p>Género: {videojuego.genero}</p>
            <p>Plataforma: {videojuego.plataforma}</p>
            <p>Clasificación: {videojuego.clasificacion || "Sin indicar"}</p>
        </article>
    );
}