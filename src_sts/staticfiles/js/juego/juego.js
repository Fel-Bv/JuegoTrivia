let numero_pregunta_actual = 1;
let $numero_pregunta_actual;
let $respuestas_correctas;
let respuestas_correctas = 0;
let $contador_preguntas;
let $formulario_juego;
let $barra_contador;
let preguntas;

function eleccion_aleatoria(lista) {return lista[Math.floor(Math.random() * lista.length)];}

function siguiente_pregunta() {
    const $pregunta_actual = document.querySelectorAll('.pregunta')[numero_pregunta_actual - 1];
    $pregunta_actual.classList.add(
        `siguiente-pregunta-${eleccion_aleatoria(['arriba', 'abajo'])}`
    );
    setTimeout(() => $pregunta_actual.classList.add('d-none'), 500);

    const es_ultima_pregunta = numero_pregunta_actual == 10;
    if (es_ultima_pregunta) return finalizar_juego();

    $barra_contador.innerHTML += '<div></div>';
    $numero_pregunta_actual.innerText = ++ numero_pregunta_actual;
}

function obtener_elementos_juego() {
    $numero_pregunta_actual = document.getElementById('pregunta-actual');
    $respuestas_correctas = document.getElementById('respuestas-correctas');
    $contador_preguntas = document.getElementById('contador');
    $formulario_juego = document.getElementById('form-preguntas');
    $barra_contador = document.getElementById('barra');
    preguntas = document.querySelectorAll('.pregunta');
}

function eventos_respuestas() {
    preguntas.forEach($pregunta => {
        $pregunta.querySelectorAll('button').forEach($btn_respuesta => {
            $btn_respuesta.onclick = evento => {
                const $btn = evento.target;
                const indice_respuesta_correcta = parseInt(
                    $btn.parentElement.parentElement.dataset.respuestaCorrecta
                );

                let indice_btn = Array.prototype.indexOf.call($btn.parentElement.children, $btn);

                [... $btn.parentElement.children][indice_respuesta_correcta]
                    .classList.replace('btn-light', 'btn-success');

                if (indice_respuesta_correcta != indice_btn)
                    $btn.classList.replace('btn-light', 'btn-danger');
                else 
                    $respuestas_correctas.value = ++ respuestas_correctas;

                setTimeout(siguiente_pregunta, 500);
            }
        });
    });
}

function finalizar_juego() {
    const $respuestas_correctas = document.createElement('h1');
    $respuestas_correctas.innerText = 'Respuestas correctas';
    $formulario_juego.append($respuestas_correctas);
    const $num_respuestas_correctas = document.createElement('h3');
    $num_respuestas_correctas.innerText = respuestas_correctas;
    $formulario_juego.append($num_respuestas_correctas);

    setTimeout(() => $formulario_juego.submit(), 2000);
}

function juego() {
    obtener_elementos_juego();
    eventos_respuestas();
}

document.readyState == 'complete'?
    juego():
    document.addEventListener('DOMContentLoaded', juego);
