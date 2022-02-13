let $contenedores_password;

function img_campo_password() {
    $contenedores_password = document.querySelectorAll('.contenedor-campo-password');
    
    $contenedores_password.forEach(
        $contenedor_password => {
            $img_campo_password = $contenedor_password.querySelector('img');
            $img_campo_password.src = `${STATIC_DIR}img/password/show.png`;
            $img_campo_password.dataset['mostrando'] = '';
        
            $img_campo_password.parentElement.onclick = evento => {
                $img = evento.target.tagName == 'figure'?
                    evento.target.querySelector('img'):
                    evento.target;
                $password = $img.parentElement.parentElement.querySelector('input');

                if ($img.dataset['mostrando']) {
                    $img.src = `${STATIC_DIR}img/password/show.png`;
                    $img.dataset['mostrando'] = '';
                    $img.alt = 'Mostrar';
                    $password.type = 'password';
        
                    return;
                }
        
                $img.src = `${STATIC_DIR}img/password/hide.png`;
                $img.dataset['mostrando'] = 'mostrando';
                $img.alt = 'Esconder';
                $password.type = 'text';
            }
        }
    )
}

document.readyState == 'complete'?
    img_campo_password():
    document.addEventListener('DOMContentLoaded', img_campo_password);
