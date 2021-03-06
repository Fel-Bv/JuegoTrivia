from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from allauth.account.utils import complete_signup
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from allauth.account import app_settings
from django.contrib import messages
from trivia.models import Pregunta, UsuarioJuego
from .puntuaciones import obtener_mejores_puntuaciones

def inicio(peticion):
    if peticion.user.is_authenticated:
        try:
            usuario_juego = [* UsuarioJuego.objects.filter(usuario=peticion.user.id)][0]
        except IndexError:
            # Probablemente el usuario se registró con allauth, por lo que no se guardó
            # un usuario en el juego.
            usuario_juego = UsuarioJuego(usuario=peticion.user).save()

        datos = {
            'usuario_juego': usuario_juego,
            'usuarios': obtener_mejores_puntuaciones(),
        }
        if peticion.user.is_superuser:
            datos['preguntas'] = Pregunta.objects.all()

        return render(peticion, 'inicio.html', datos)
    
    return redirect('usuarios:iniciar_sesion')

def registro(peticion):
    logout(peticion)

    if peticion.method == 'POST':
        formulario = UserCreationForm(peticion.POST)
        if formulario.is_valid():
            formulario.instance.email = peticion.POST['email']
            usuario = formulario.save()

            usuario_juego = UsuarioJuego(usuario=usuario)
            usuario_juego.save()

            # login(peticion, usuario, backend='django.contrib.auth.backends.ModelBackend')

            # return redirect('usuarios:inicio')

            return complete_signup(peticion, usuario, app_settings.EMAIL_VERIFICATION, '/')

        messages.error(peticion, formulario.errors)

        formulario = UserCreationForm()
        formulario.set_password1_help_text()
        return render(peticion, 'usuarios/registro.html', {
            'formulario': formulario,
        })

    formulario = UserCreationForm()
    return render(peticion, 'usuarios/registro.html', {
        'formulario': formulario,
    })

def iniciar_sesion(peticion):
    logout(peticion)

    if peticion.method == 'POST':
        formulario = AuthenticationForm(peticion, peticion.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()

            login(peticion, usuario, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('usuarios:inicio')

        for error in formulario.get_invalid_login_error():
            messages.error(peticion, error)

    formulario = AuthenticationForm()
    return render(peticion, 'usuarios/iniciar_sesion.html', {
        'formulario': formulario,
    })
