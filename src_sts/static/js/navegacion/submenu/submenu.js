let $contenedor_submenu;
let $boton_submenu;

function submenu() {
    $contenedores_submenu = document.querySelectorAll('.contenedor-submenu');
    $contenedores_submenu.forEach($contenedor_submenu => {
        $boton_submenu = $contenedor_submenu.parentElement;
        $boton_submenu.onclick = () => {
            $contenedor_submenu.classList.toggle('d-none');
        }
    });
}

document.readyState == 'complete'?
    submenu():
    document.addEventListener('DOMContentLoaded', submenu)
