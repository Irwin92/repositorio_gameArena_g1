export default function VideojuegoCard({
    videojuego,
    onEditar,
    onEliminar,
}) {
    return (
        <div className="col-md-4 col-lg-4">
            <div className="card h-100 shadow-sm">
                <div className="card-body">
                    <h3 className="h5 card-title">
                        {videojuego.nombre}
                    </h3>
                    <p className="card-text mb-1">
                        <strong>Género:</strong> {videojuego.genero}
                    </p>
                    <p className="card-text mb-1">
                        <strong>Plataforma:</strong> {videojuego.plataforma}
                    </p>
                    <p className="card-text mb-3">
                        <strong>Clasificación:</strong> {""}
                        {videojuego.clasificacion || "Sin indicar"}
                    </p>
                    <div className="d-flex gap-2">
                        <button className="btn btn-outline-primary btn-sm"
                            onClick={() => onEditar(videojuego)}
                        >
                            Editar
                        </button>

                        <button className="btn btn-danger btn-sm"
                            onClick={() => onEliminar(videojuego.id)}
                        >
                            Eliminar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}