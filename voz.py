import speech_recognition as sr
from gtts import gTTS

def devolver_numero(texto):
    numeros = {
        'uno': 1,
        'dos': 2,
        'tres': 3,
        'cuatro': 4,
        'cinco': 5,
        'seis': 6,
        'siete': 7,
        'ocho': 8,
        'nueve': 9
    }
    palabras = texto.lower().split()

    for palabra in palabras:
        if palabra.isdigit():
            return int(palabra)

    for i in range(len(palabras)):
        if palabras[i] == 'piso' and i + 1 < len(palabras):
            return numeros.get(palabras[i + 1], None)

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def reproducir_audio(mensaje):
    tts = gTTS(text=mensaje, lang='es')
    tts.save("mensaje.mp3")
    audio = AudioSegment.from_mp3("mensaje.mp3")
    play(audio)

def reconocer_voz():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            texto = recognizer.recognize_google(audio, language="es")

            if "espejito espejito" in texto.lower():
                print("Escuchando...")
                mensaje_despues_activacion = texto.split("espejito espejito", 1)[1].strip()
                print(mensaje_despues_activacion)

                if "piso" in mensaje_despues_activacion.lower():
                    numero_piso = devolver_numero(mensaje_despues_activacion)

                    if numero_piso is not None and 1 <= numero_piso <= 9:
                        mensaje_reproduccion = f"Vamos al piso {numero_piso}"
                        print(mensaje_reproduccion)
                        reproducir_audio(mensaje_reproduccion)
                        break
                    else:
                        mensaje_reproduccion = "En este edificio solo hay 9 pisos."
                        print(mensaje_reproduccion)
                        reproducir_audio(mensaje_reproduccion)

        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
        except sr.RequestError as e:
            print("Error al enviar la solicitud al servicio de reconocimiento de voz; {0}".format(e))

if __name__ == "__main__":
    reconocer_voz()
