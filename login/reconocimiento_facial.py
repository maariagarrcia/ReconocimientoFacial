import face_recognition as fr
import os
import random
import cv2
import numpy as np
import mediapipe as mp
import time
import tkinter as tk

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

class ReconocimientoFacial:
    def __init__(self):
        self.image_folder = "media/profiles"
        self.images = []
        self.clases = []
        self.lista = os.listdir(self.image_folder)
        self.comp1 = 100
        self.tiempo_usuario_actual = 0
        self.tiempo_limite_usuario = 4
        self.ventana_reconocimiento = tk.Tk()
        self.ventana_gestos = None
        self.label_usuario = tk.Label(self.ventana_reconocimiento, text="")
        self.label_usuario.pack()

        for lis in self.lista:
            imgdb = cv2.imread(f"{self.image_folder}/{lis}")
            self.images.append(imgdb)
            self.clases.append(os.path.splitext(lis)[0])

    def codrostros(self, images):
        listacod = []
        for img in images:
            try:
                if img is None or img.size == 0:
                    print("Error: La imagen está vacía o no se ha cargado correctamente.")
                    continue

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                cod = fr.face_encodings(img)[0]
                listacod.append(cod)
            except (IndexError, cv2.error, fr.FaceEncodingsError) as e:
                print(f"Error en la conversión de color o codificación facial: {e}")
        return listacod

    def horario(self, nombre):
        # Implementa la lógica para registrar la hora
        pass

    def abrir_ventana_gestos(self, nombre):
        self.ventana_reconocimiento.withdraw()
        self.ventana_gestos = tk.Toplevel()
        self.ventana_gestos.title("A qué piso desea ir?")
        etiqueta_pregunta = tk.Label(self.ventana_gestos, text=f"Hola {nombre} ¿A qué piso quieres ir?")
        etiqueta_pregunta.pack()

        self.gestos = Gestos(self.ventana_gestos, nombre)
        self.gestos.iniciar_gestos()

    def actualizar_label_usuario(self, nombre):
        self.label_usuario.config(text=f"Bienvenido, {nombre}!")

    def iniciar_reconocimiento(self):
        rostroscod = self.codrostros(self.images)
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            frame2 = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            faces = fr.face_locations(rgb)
            facescod = fr.face_encodings(rgb, faces)

            for facecod, faceloct in zip(facescod, faces):
                comparacion = fr.compare_faces(rostroscod, facecod)
                simi = fr.face_distance(rostroscod, facecod)

                if len(simi) > 0:
                    min_index = np.argmin(simi)
                    if comparacion[min_index]:
                        nombre = self.clases[min_index].upper()
                        yi, xf, yf, xi = faceloct
                        yi, xf, yf, xi = yi * 4, xf * 4, yf * 4, xi * 4

                        if self.comp1 != min_index:
                            r = random.randrange(0, 255, 50)
                            g = random.randrange(0, 255, 50)
                            b = random.randrange(0, 255, 50)
                            self.comp1 = min_index
                            self.tiempo_usuario_actual = time.time()

                        if self.comp1 == min_index:
                            cv2.rectangle(frame, (xi, yi), (xf, yf), (r, g, b), 3)
                            cv2.rectangle(frame, (xi, yf - 35), (xf, yf), (r, g, b), cv2.FILLED)
                            cv2.putText(frame, nombre, (xi + 6, yf - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                            self.horario(nombre)
                            self.actualizar_label_usuario(nombre)

                            tiempo_actual = time.time()
                            tiempo_transcurrido = tiempo_actual - self.tiempo_usuario_actual

                            if tiempo_transcurrido > self.tiempo_limite_usuario:
                                self.abrir_ventana_gestos(nombre)

            cv2.imshow("Ventana de Reconocimiento", frame)
            t = cv2.waitKey(5)
            if t == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        hands.close()



class Gestos:
    def __init__(self, ventana, nombre_usuario):
        self.ventana_gestos = ventana
        self.nombre_usuario = nombre_usuario
        self.tiempo_inicio_gesto = 0
        self.tiempo_limite_gesto = 3  # 3 segundos de tiempo límite para un gesto

    

    @staticmethod
    def detectar_gesto(landmarks):
        dedo_indicador = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        dedo_pulgar = landmarks[mp_hands.HandLandmark.THUMB_TIP]
        dedo_medio = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        dedo_anular = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
        dedo_menique = landmarks[mp_hands.HandLandmark.PINKY_TIP]

        # Distancias entre los dedos y el pulgar
        dist_thumb_indicador = np.linalg.norm(
            np.array([dedo_pulgar.x, dedo_pulgar.y, dedo_pulgar.z]) -
            np.array([dedo_indicador.x, dedo_indicador.y, dedo_indicador.z])
        )
        dist_thumb_medio = np.linalg.norm(
            np.array([dedo_pulgar.x, dedo_pulgar.y, dedo_pulgar.z]) -
            np.array([dedo_medio.x, dedo_medio.y, dedo_medio.z])
        )
        dist_thumb_anular = np.linalg.norm(
            np.array([dedo_pulgar.x, dedo_pulgar.y, dedo_pulgar.z]) -
            np.array([dedo_anular.x, dedo_anular.y, dedo_anular.z])
        )
        dist_thumb_menique = np.linalg.norm(
            np.array([dedo_pulgar.x, dedo_pulgar.y, dedo_pulgar.z]) -
            np.array([dedo_menique.x, dedo_menique.y, dedo_menique.z])
        )

        # Umbral para considerar el puño cerrado
        umbral_puno = 0.02

        # Detectar el puño cerrado
        if (
            dist_thumb_indicador < umbral_puno and
            dist_thumb_medio < umbral_puno and
            dist_thumb_anular < umbral_puno and
            dist_thumb_menique < umbral_puno
        ):
            return "puño_cerrado"

        # Contar dedos levantados
        dedos_levantados = 0

        # Umbral para considerar el dedo levantado
        umbral_dedo_levantado = 0.05

        # Analizar cada dedo
        if dedo_indicador.y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y - umbral_dedo_levantado:
            dedos_levantados += 1
        if dedo_medio.y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y - umbral_dedo_levantado:
            dedos_levantados += 1
        if dedo_anular.y < landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y - umbral_dedo_levantado:
            dedos_levantados += 1
        if dedo_menique.y < landmarks[mp_hands.HandLandmark.PINKY_MCP].y - umbral_dedo_levantado:
            dedos_levantados += 1

        return dedos_levantados

    def procesar_gesto(self, gesto):
        if gesto > 0:
            print(f"Dedos levantados: {gesto}.")
           
            self.tiempo_inicio_gesto = 0

            # Actuar según el número de dedos levantados, por ejemplo:
            print(f"¡Perfecto! Vamos al piso {gesto}.")

    def iniciar_gestos(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmarks = hand_landmarks.landmark
                    gesto = self.detectar_gesto(landmarks)

                    if gesto > 0:
                        tiempo_actual = time.time()

                        if self.tiempo_inicio_gesto == 0:
                            self.tiempo_inicio_gesto = tiempo_actual
                        elif tiempo_actual - self.tiempo_inicio_gesto > self.tiempo_limite_gesto:
                            # Realizar la acción cuando el gesto se mantiene durante más de 3 segundos
                            self.procesar_gesto(gesto)

                            # Restablecer el tiempo del gesto
                            self.tiempo_inicio_gesto = 0

            cv2.imshow("A que piso deseas ir?", frame)
            t = cv2.waitKey(5)
            if t == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        hands.close()



if __name__ == "__main__":
    reconocimiento = ReconocimientoFacial()  
    reconocimiento.iniciar_reconocimiento()

    # Agregar la instanciación de la clase Gestos
    if reconocimiento.ventana_gestos:
        gestos = Gestos(reconocimiento.ventana_gestos)  
        gestos.iniciar_gestos()
