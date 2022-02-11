from django.utils.translation import gettext as _
from django.db import models

class Pregunta(models.Model):
    texto = models.TextField(
        verbose_name=_('Pregunta'),
        name='texto',
        max_length=255,
        editable=False,
        blank=False,
        null=False,
        help_text=''
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
