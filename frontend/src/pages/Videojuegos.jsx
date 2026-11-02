import { useEffect, useState } from "react";
import VideojuegoCard from "../components/VideojuegoCard";

const API_URL = "http://127.0.0.1:8000/api/videojuegos/";

export default function Videojuegos() {
    const [videojuegos, setVideojuegos] = useState([]);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState("");

    const formularioInicial = {
        nombre: "",
        genero: "",
        plataforma: "PC",
        clasificacion: "",
        fecha_lanzamiento: "",
        activo: true,
    }

    const [formulario, setFormulario] = useState(formularioInicial);
    const [editandoId, setEditandoId] = useState(null);
    const [mensaje, setMensaje] = useState("");
    const [procesando, setProcesando] = useState(false);


    useEffect(() => {
        async function cargarVideojuegos() {
            try {
                setCargando(true);
                setError("");

                const respuesta = await fetch(API_URL);
                if (!respuesta.ok) {
                    throw new Error(`Error HTTP: ${respuesta.status}`);
                }

                const datos = await respuesta.json();
                setVideojuegos(datos);
            } catch (err) {
                setError(err.message);
            } finally {
                setCargando(false);
            }
        }
        cargarVideojuegos();
    }, []);

    const videojuegosPC = videojuegos.filter(
        (videojuego) => videojuego.plataforma === "PC"
    );

    if (cargando) return <p>Cargando videojuegos...</p>;

    if (error) return <p>Error:{error}</p>;
    /** ----------------------------funcion de manejar cambios----------------------------------------------- */
    function manejarCambio(e) {
        const { name, value, type, checked } = e.target;

        /*name indica que propiedad debe cambiar       
        value contiene el texto o valor seleccionado
        checked se utiliza para el checkbox activo
        ... formulario conserva los demas campos
        */
        setFormulario({
            ...formulario,
            [name]: type === "checkbox" ? checked : value,
        });
    }

    /** ----------------------------funcion de crear videojuego----------------------------------------------- */
    async function crearVideojuego() {
        const respuesta = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "aplication/json",
            },
            body: JSON.stringify(formulario),
        });
        if (!respuesta.ok) {
            throw new Error("No se pudo crear el videojuego")
        }
        const nuevo = await respuesta.json();
        setVideojuegos((actuales) => [...actuales, nuevo]);
    }

    /** ----------------------------funcion para validar campos minimos----------------------------------------------- */
    function validadFormulario() {
        if (!formulario.nombre.trim()) {
            setError("El nombre es obligatorio");
            return false;
        }
        if (!formulario.plataforma) {
            setError("Debe seleccionar una plataforma");
            return false;
        }
        return true;
    }
    /** ----------------------------funcion para iniciar edicion----------------------------------------------- */
    function iniciarEdicion(videojuego) {
        setEditandoId(videojuego.id);
        setFormulario({
            nombre: videojuego.nombre ?? "",
            genero: videojuego.genero ?? "",
            plataforma: videojuego.plataforma ?? "PC",
            clasificacion: videojuego.clasificacion ?? "",
            fecha_lanzamiento: videojuego.fecha_lanzamiento ?? "",
            activo: videojuego.activo ?? true,
        });
        setMensaje("");
        setError("");
    }

    /** ----------------------------funcion para actualizar----------------------------------------------- */
    async function actualizarVideojuego() {
        const respuesta = await fetch(
            `${API_URL}${editandoId}/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "aplication/json",
            },
            body: JSON.stringify(formulario),
        });
        if (!respuesta.ok) {
            throw new Error("No se pudo actualziar el videojuego")
        }

        const actualizado = await respuesta.json();

        setVideojuegos((actuales) =>
            actuales.map((videojuego) =>
                videojuego.id === actualizado.id
                    ? actualizado
                    : videojuego
            )
        );
    }//Fin de la funcion actualizar
    /** ----------------------------funcion para guardar un video juego ya sea recien creado oa actualizado----------------------------------------------- */
    async function guardarVideojuego(e) {
        e.preventDefault();

        if (!validadFormulario()) return;
        try {
            setProcesando(true);
            setError("");
            setMensaje("");

            if (editandoId === null) {
                await crearVideojuego();
                setMensaje("Videojuego creado correctamente")
            } else {
                await actualizarVideojuego();
                setMensaje("Videojuego actualizado correctamente")
            }

            setFormulario(formularioInicial);
            setEditandoId(null);

        } catch (err) {
            setError(err.message);
        } finally {
            setProcesando(false);
        }
    }
    /** ----------------------------funcion para Cancelar edicion----------------------------------------------- */
    function cancelarEdicion() {
        setEditandoId(null);
        setFormulario(formulario);
        setError("");
        setMensaje("");
    }
    /** ----------------------------funcion asyn para eliminar con Delete----------------------------------------------- */
    async function eliminarVideojuego(id) {
        const confirmar = window.confirm("¿Desea eliminar este videojuego?");

        if (!confirmar) return;
        try {
            setError("");
            setMensaje("");

            const respuesta = await fetch(
                `${API_URL}${id}/`, {
                method: "DELETE"
            });
            if (!respuesta.ok) {
                throw new Error("No se pudo eliminar el videojuego")
            }

            setVideojuegos((actuales) =>
                actuales.filter((videojuego) => videojuego.id !== id)
            );
            if(editandoId ===id){
                cancelarEdicion();
            }
            setMensaje("Videojuego eliminado correctamente");
        } catch (err) {
            setError(err.message);
        }
    }

    /**++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
    return (
        <form onSubmit={guardarVideojuego} className="card card-body mb-4">
            <h2 className="h4 mb-3">{editandoId ? "Editar videojuego" : "Nuevo videojuego"}</h2>
            <div className="mb-3">
                <label className="form-label">Nombre</label>
                <input className="form-control"
                    name="nombre"
                    value={formulario.nombre}
                    onChange={manejarCambio}
                />
            </div>
            <div className="mb-3">
                <label className="form-label">Género</label>
                <input className="form-control"
                    name="genero"
                    value={formulario.genero}
                    onChange={manejarCambio}
                />
            </div>
            <div className="mb-3">
                <label className="form-label">Plataforma</label>
                <select className="form-select"
                    name="plataforma"
                    value={formulario.plataforma}
                    onChange={manejarCambio}
                >
                    <option value="PC">PC</option>
                    <option value="PlayStation">PlayStation</option>
                    <option value="Xbox">Xbox</option>
                    <option value="Nintendo">Nintendo</option>
                </select>
            </div>

            <div className="mb-3">
                <label className="form-label">Clasificación</label>
                <input className="form-control"
                    name="clasificacion"
                    value={formulario.clasificacion}
                    onChange={manejarCambio}
                />
            </div>
            <div className="mb-3">
                <label className="form-label">Fecha de lanzamiento</label>
                <input type="date"
                    className="form-control"
                    name="fecha_lanzamiento"
                    value={formulario.fecha_lanzamiento}
                    onChange={manejarCambio}
                />
            </div>
            <div className="form-check mb-3">
                <input className="form-check-input"
                    type="checkbox"
                    name="activo"
                    value={formulario.activo}
                    onChange={manejarCambio}
                />
                <label className="form-check-label">Activo</label>
            </div>
            <div className="d-flex gap-2">
                <button className="btn btn-primary" disabled={procesando} >
                    {procesando
                        ? "Procesando..."
                        : editandoId
                            ? "Actualizar"
                            : "Guardar"}
                </button>
                {editandoId && (
                    <button type="button" className="btn btn-secondary" onClick={cancelarEdicion}>
                        Cancelar
                    </button>
                )}
            </div>
        </form>/*
        <section>
            <h2>Videojuegos disponibles</h2>
            {videojuegos.length === 0 ? (
                <p>No hay videojuegos disponibles</p>
            ) : (
                videojuegos.map((videojuego) => (
                    <VideojuegoCard
                        key={videojuego.id}
                        videojuego={videojuego}
                    />
                ))
            )}
            <h2>Videojuegos de PC</h2>
            {videojuegosPC.map((videojuego) => (
                <p key={videojuego.id}>
                    {videojuego.nombre} - {videojuego.plataforma}
                </p>
            ))}
        </section>*/

    );
}