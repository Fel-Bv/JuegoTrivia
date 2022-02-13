from usuarios.puntuaciones import obtener_mejores_puntuaciones
from django.utils.translation import gettext
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Pregunta, UsuarioJuego
import random
import string
import json

def validar_no_existencia_pregunta(peticion, pregunta):
    # Validación de que la pregunta no está registrada aún:
    preguntas_registradas = [pregunta.texto for pregunta in Pregunta.objects.all()]
    caracteres_admitidos = string.ascii_lowercase + string.digits
    acentos = {
        'a': 'á',
        'e': 'é',
        'i': 'í',
        'o': 'ó',
        'u': 'ú',
    }
    for pregunta_registrada in preguntas_registradas:
        pregunta_registrada = pregunta_registrada.lower()
        pregunta = pregunta.lower()

        _pregunta_registrada = ''
        _pregunta = ''
        for caracter in pregunta_registrada:
            for caracter_admitido in caracteres_admitidos:
                if caracter == caracter_admitido:
                    _pregunta_registrada += caracter

            for letra in acentos.keys():
                if caracter == acentos[letra]:
                    _pregunta_registrada += letra

        for caracter in pregunta:
            for caracter_admitido in caracteres_admitidos:
                if caracter == caracter_admitido:
                    _pregunta += caracter

            for letra in acentos.keys():
                if caracter == acentos[letra]:
                    _pregunta += letra

        if _pregunta == _pregunta_registrada:
            messages.error(peticion, 'Esta pregunta ya está registrada.')
            return redirect('trivia:crear_pregunta')


def crear_pregunta(peticion):
    if not peticion.user.is_authenticated:
        return redirect('usuarios:iniciar_sesion')

    if peticion.method == 'POST':
        respuesta_correcta = int(peticion.POST['respuesta_correcta'])
        respuestas = json.loads(peticion.POST['respuestas'])
        pregunta = peticion.POST['pregunta']

        pregunta_existente = validar_no_existencia_pregunta(peticion, pregunta)
        if pregunta_existente:
            return pregunta_existente

        # Valida que el indice de la respuesta correcta no sea mayor al número de respuestas:
        if respuesta_correcta + 1 > len(respuestas):
            messages.error(
                peticion,
                'Índice de respuesta correcta mayor a la cantidad de respuestas.'
            )
            return redirect('trivia:crear_pregunta')

        pregunta = Pregunta(
            texto=pregunta,
            respuestas=respuestas,
            respuesta_correcta=respuesta_correcta
        )
        pregunta.save()

        messages.success(peticion, 'Se ha agregado tu pregunta.')
        return redirect('trivia:crear_pregunta')

    return render(peticion, 'trivia/crear_pregunta.html')

def jugar(peticion):
    if not peticion.user.is_authenticated:
        return redirect('usuarios:iniciar_sesion')

    if peticion.method == 'POST':
        usuario_juego = [* UsuarioJuego.objects.filter(usuario=peticion.user.id)][0]
        respuestas_correctas = int(peticion.POST['respuestas_correctas'])
        if respuestas_correctas <= 5:
            mensaje = f'Tuviste {respuestas_correctas} respuesta'
            mensaje += 's ' if respuestas_correctas > 1 else ' '
            mensaje += 'correcta'
            mensaje += 's.' if respuestas_correctas > 1 else '.'
            messages.error(peticion, gettext(mensaje))
        else:
            mensaje = f'Tuviste {respuestas_correctas} respuesta'
            mensaje += 's ' if respuestas_correctas > 1 else ' '
            mensaje += 'correcta'
            mensaje += 's.' if respuestas_correctas > 1 else '.'
            messages.success(peticion, gettext(mensaje))

        usuario_juego.puntuacion_actual += respuestas_correctas * 10
        try:
            usuario_juego.nivel_juego = usuario_juego.puntuacion_actual // 200
        except ZeroDivisionError:
            pass
        usuario_juego.save()

        return redirect('trivia:tablero_puntuacion')

    preguntas = random.sample([* Pregunta.objects.all()], 10)

    return render(peticion, 'trivia/jugar.html', {
        'preguntas': preguntas,
    })

def tablero_puntuacion(peticion):
    if not peticion.user.is_authenticated:
        return redirect('usuarios:iniciar_sesion')

    return render(peticion, 'trivia/tablero_puntuacion.html', {
        'usuarios': obtener_mejores_puntuaciones(),
    })
