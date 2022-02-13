function mensajes() {
    const mensajes = document.querySelectorAll('.mensaje');

    if (! mensajes) return;

    mensajes.forEach($mensaje => {
        $mensaje.classList.add('desaparecer');
        setTimeout(() => $mensaje.remove(), 6000);
    });
}

document.readyState == 'complete'?
    mensajes():
    document.addEventListener('DOMContentLoaded', mensajes);
