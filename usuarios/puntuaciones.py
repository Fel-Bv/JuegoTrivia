from django.contrib.auth.models import User

def obtener_mejores_puntuaciones():
    usuarios = [* User.objects.all()]
    if len(usuarios) > 10: usuarios = usuarios[:10]

    cambio = True
    while cambio:
        cambio = False
        for i in range(len(usuarios[:-1])):
            if usuarios[i + 1].puntuacion_actual > usuarios[i].puntuacion_actual:
                cambio = True
                usuarios[i + 1], usuarios[i] = usuarios[i], usuarios[i + 1]

    return usuarios
