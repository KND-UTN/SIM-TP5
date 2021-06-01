import math

from .randoms import Random


class Eventos:
    def __init__(self):
        self.rnd_tiempo_llegada = None
        self.tiempo_llegada = None
        self.prox_llegada = math.inf

        self.rnd_tiempo_examen = None
        self.tiempo_examen = None
        self.fin_examen = math.inf

        self.rnd_tiempo_atencion = None
        self.tiempo_atencion = None
        self.fin_atencion_m1 = math.inf
        self.fin_atencion_m2 = math.inf

        self.rnd_urgente = None
        self.urgente = None

        # Inicializamos los eventos procesando cuando va a ser la proxima llegada.
        self.calcular_proxima_llegada(0)

    def calcular_proxima_llegada(self, reloj):
        self.rnd_tiempo_llegada = Random().randomLlegada()
        self.tiempo_llegada = 2 + self.rnd_tiempo_llegada * (6)
        self.prox_llegada = reloj + self.tiempo_llegada

    def calcular_fin_examen(self, reloj):
        self.rnd_tiempo_examen = Random().randomExamen()
        self.tiempo_examen = 3 + self.rnd_tiempo_examen * (14)
        self.fin_examen = reloj + self.tiempo_examen

    def calcular_fin_atencion_m1(self, reloj):
        self.rnd_tiempo_atencion = Random().randomAtencion()
        self.tiempo_atencion = 6 + self.rnd_tiempo_atencion * (8)
        self.fin_atencion_m1 = reloj + self.tiempo_atencion

    def calcular_fin_atencion_m1_con_remanencia(self, reloj, remanencia):
        self.fin_atencion_m1 = reloj + remanencia

    def calcular_fin_atencion_m2_con_remanencia(self, reloj, remanencia):
        self.fin_atencion_m2 = reloj + remanencia

    def calcular_fin_atencion_m2(self, reloj):
        self.rnd_tiempo_atencion = Random().randomAtencion()
        self.tiempo_atencion = 6 + self.rnd_tiempo_atencion * (8)
        self.fin_atencion_m2 = reloj + self.tiempo_atencion

    def calcular_urgente(self):
        self.rnd_urgente = Random().randomCaso()
        self.urgente = self.rnd_urgente < .4
        return self.urgente

    def arrastrar_llegada_paciente(self):
        self.rnd_tiempo_llegada = None
        self.tiempo_llegada = None

    def arrastrar_fin_examen(self):
        self.rnd_tiempo_examen = None
        self.tiempo_examen = None

    def arrastrar_fin_atencion(self):
        self.rnd_tiempo_atencion = None
        self.tiempo_atencion = None

    def limpiar_fin_examen(self):
        self.rnd_tiempo_examen = None
        self.tiempo_examen = None
        self.fin_examen = math.inf

    def limpiar_fin_atencion_m1(self):
        self.rnd_tiempo_atencion = None
        self.tiempo_atencion = None
        self.fin_atencion_m1 = math.inf

    def limpiar_fin_atencion_m2(self):
        self.rnd_tiempo_atencion = None
        self.tiempo_atencion = None
        self.fin_atencion_m2 = math.inf

    def limpiar_urgente(self):
        self.rnd_urgente = None
        self.urgente = None

    def get_proximo_evento(self):
        eventos_posibles = {"llegada_paciente": self.prox_llegada, "fin_examen": self.fin_examen,
                            "fin_atencion (M1)": self.fin_atencion_m1, "fin_atencion (M2)": self.fin_atencion_m2}
        siguiente_evento = min(eventos_posibles, key=eventos_posibles.get)
        siguiente_reloj = eventos_posibles[siguiente_evento]
        return siguiente_reloj, siguiente_evento

    def get_fila(self):
        llegada_paciente = [self.rnd_tiempo_llegada, self.tiempo_llegada, self.prox_llegada]
        fin_examen = [self.rnd_tiempo_examen, self.tiempo_examen, self.fin_examen]
        urgente = [self.rnd_urgente, self.urgente]
        fin_atencion = [self.rnd_tiempo_atencion, self.tiempo_atencion, self.fin_atencion_m1, self.fin_atencion_m2]
        return llegada_paciente + fin_examen + urgente + fin_atencion
