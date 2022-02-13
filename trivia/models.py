import imp
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db import models

class Pregunta(models.Model):
    texto = models.TextField(
        verbose_name=_('Pregunta'),
        name='texto',
        max_length=255,
        blank=False,
        null=False,
        help_text=_('Text')
    )
    respuestas = models.JSONField(
        verbose_name=_('Respuestas'),
        name='respuestas',
    )
    respuesta_correcta = models.IntegerField(
        verbose_name=_('Respuesta correcta'),
        help_text=_('Respuesta correcta'),
        name='respuesta_correcta',
    )

    def __str__(self):
        return f'{self.texto}: {self.respuestas[self.respuesta_correcta]}'

class UsuarioJuego(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        to_field='id',
        verbose_name=_('User ID')
    )
    # Propiedades del juego
    puntuacion_actual = models.IntegerField(_('Current score'), default=0, null=True)
    nivel_juego = models.IntegerField(_('Game level'), default=0, null=True)

    def __str__(self):
        return f'{self.usuario}, {self.puntuacion_actual} - {self.nivel_juego}'
