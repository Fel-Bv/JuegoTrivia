from usuarios.puntuaciones import obtener_mejores_puntuaciones
from django.utils.translation import gettext
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Pregunta
import random
import json

def crear_pregunta(peticion):
    if not peticion.user.is_authenticated:
        return redirect('usuarios:iniciar_sesion')

    if peticion.method == 'POST':
        respuesta_correcta = int(peticion.POST['respuesta_correcta'])
        respuestas = json.loads(peticion.POST['respuestas'])
        pregunta = peticion.POST['pregunta']

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

        peticion.user.puntuacion_actual += respuestas_correctas * 10
        try:
            peticion.user.nivel_juego = peticion.user.puntuacion_actual // 200
        except ZeroDivisionError:
            pass
        peticion.user.save()

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
