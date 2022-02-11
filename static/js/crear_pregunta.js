let $input_respuesta_correcta;
let $respuesta_correcta;
let $input_respuestas;
let $nueva_respuesta;
let $btn_formulario;
let $respuestas;
let $formulario;

function crear_evento_respuesta_correcta() {
    $respuestas.querySelectorAll('.respuesta-correcta').forEach($btn_respuesta_correcta => {
        $btn_respuesta_correcta.onclick = evento => {
            $respuestas.querySelectorAll('input').forEach($input_respuesta => {
                $input_respuesta.dataset['correcto'] = '';
            });

            let $respuesta = evento.target.parentElement;
            while ($respuesta.tagName != 'DIV') {
                $respuesta = $respuesta.parentElement;
            }
            $respuesta.querySelector('input').dataset['correcto'] = true;
            $respuesta_correcta = $respuesta;
        }
    });
}

function eventos_crear_pregunta() {
    $input_respuesta_correcta = document.querySelector('input[name="respuesta_correcta"]');
    $input_respuestas = document.querySelector('input[name="respuestas"]');
    $nueva_respuesta = document.getElementById('nueva-respuesta');
    $btn_formulario = document.getElementById('enviar-formulario');
    $formulario = document.getElementById('form-crear-pregunta');
    $respuestas = document.getElementById('respuestas');
    $respuesta_correcta = $respuestas.querySelector('.respuesta');

    $nueva_respuesta.onclick = () => {
        if ([... $respuestas.children].length == 5) return;

        const $respuesta = document.createElement('div');
        $respuesta.classList.add('respuesta');
        $respuesta.innerHTML = `
            <input type="text" class="form-control" maxlength="100">
            <button type="button" class="btn btn-success respuesta-correcta">
                <img
                    src="${STATIC_DIR}img/check.png"
                    alt="Respuesta correcta"
                >
            </button>
        `;
        $respuestas.append($respuesta);

        const respuestas = $respuestas.querySelectorAll('input');
        respuestas[respuestas.length - 1].focus();

        if ([... $respuestas.children].length == 5) $nueva_respuesta.disabled = true;

        crear_evento_respuesta_correcta();
    }

    $btn_formulario.onclick = () => {
        let respuesta_correcta = Array.prototype.indexOf.call(
            $respuestas.children, $respuesta_correcta
        );
        $input_respuesta_correcta.value = respuesta_correcta;

        const respuestas = [];
        $respuestas.querySelectorAll('input').forEach($input_respuesta => {
            respuestas.push($input_respuesta.value);
        });
        $input_respuestas.value = JSON.stringify(respuestas);

        $formulario.submit();
    }

    crear_evento_respuesta_correcta();
}

document.readyState == 'complete'?
    eventos_crear_pregunta():
    document.addEventListener('DOMContentLoaded', eventos_crear_pregunta);
