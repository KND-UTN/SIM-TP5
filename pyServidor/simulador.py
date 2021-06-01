from clases.randoms import Random
from clases.eventos import Eventos
from clases.enfermero import Enfermero
from clases.medicos import Medicos
from clases.estadisticas import Estadisticas
from clases.administradorPacientes import AdministradorPacientes

import pandas as pd


class Simulacion:

    def __init__(self, cant_filas):
        # Inicializamos la fila
        self.nombre_evento = 'Inicializacion'
        self.reloj = 0
        self.eventos = Eventos()
        self.enfermero = Enfermero()
        self.medicos = Medicos()
        estadisticas = Estadisticas()
        self.pacientes = AdministradorPacientes()

        self.fila = [[self.nombre_evento, self.reloj] + \
                     self.eventos.get_fila() + self.enfermero.get_fila() + self.medicos.get_fila()]
        columnas = ["nombre_evento", "reloj", "rnd_llegada", "tiempo_llegada", "proxima_llegada", "rnd_examen",
                    "tiempo_examen", "proximo_examen", "rnd_urgente", "urgente", "rnd_atencion", "tiempo_atencion",
                    "fin_atencion_m1", "fin_atencion_m2", "estado", "cola", "estado_M1", "estado_M2", "cola_comun",
                    "cola_urgente"]
        self.tabla = pd.DataFrame(self.fila, columns=columnas)

        for n in range(cant_filas):
            self.proxima_fila()

            # Solo si hay que mostrar la linea, hacemos esto
            self.fila = [self.nombre_evento, self.reloj] + \
                        self.eventos.get_fila() + self.enfermero.get_fila() + self.medicos.get_fila()
            self.tabla = self.tabla.append(pd.DataFrame([self.fila], columns=columnas))
            # Hasta aca

        self.reloj, proximo_evento = self.eventos.get_proximo_evento()
        print(proximo_evento)

    def proxima_fila(self):
        self.reloj, self.nombre_evento = self.eventos.get_proximo_evento()
        if self.nombre_evento == "llegada_paciente":
            self.llegada_paciente()
        elif self.nombre_evento == "fin_examen":
            self.fin_examen()
        elif self.nombre_evento == "fin_atencion (M1)":
            self.fin_atencion_m1()
        elif self.nombre_evento == "fin_atencion (M2)":
            self.fin_atencion_m2()
        else:
            raise Exception("FATAL ERROR: Por alguna razon, no hay proximo evento.")

    def llegada_paciente(self):
        self.eventos.calcular_proxima_llegada(self.reloj)
        nuevo_paciente = self.pacientes.nuevo_paciente(self.reloj)
        if self.enfermero.add_paciente(nuevo_paciente) == 1:  # El paciente fue atendido en el momento
            self.eventos.calcular_fin_examen(self.reloj)
        else:
            self.eventos.arrastrar_fin_examen()
        self.eventos.arrastrar_fin_atencion()
        self.eventos.limpiar_urgente()

    def fin_examen(self):
        self.eventos.arrastrar_llegada_paciente()
        paciente_examinado = self.enfermero.atender_siguiente()
        if self.enfermero.esta_ocupado():  # Si hay alguien en la cola y se lo acaba de empezar a examinar
            self.eventos.calcular_fin_examen(self.reloj)
        else:  # No habia nadie en la cola -> no se esta examinando a nadie
            self.eventos.limpiar_fin_examen()
        urgente = self.eventos.calcular_urgente()
        if urgente:
            paciente_examinado.caso.urgencia(paciente_examinado)
            fue_atendido = self.medicos.nuevo_urgencia(paciente_examinado, self.reloj, self.eventos.fin_atencion_m1)
        else:
            paciente_examinado.caso.caso_comun(paciente_examinado)
            fue_atendido = self.medicos.nuevo_comun(paciente_examinado)

        if fue_atendido == 1:
            self.eventos.calcular_fin_atencion_m1(self.reloj)
        elif fue_atendido == 2:
            self.eventos.calcular_fin_atencion_m2(self.reloj)
        else:
            self.eventos.arrastrar_fin_atencion()

    def fin_atencion_m1(self):
        self.eventos.arrastrar_llegada_paciente()
        self.eventos.arrastrar_fin_examen()
        self.eventos.limpiar_urgente()
        atendido_suspendido = self.medicos.siguiente_m1()
        if not atendido_suspendido:
            if self.medicos.medico1_esta_ocupado():
                self.eventos.calcular_fin_atencion_m1(self.reloj)
            else:
                self.eventos.limpiar_fin_atencion_m1()
        else:
            self.eventos.calcular_fin_atencion_m1_con_remanencia(self.reloj, self.medicos.tiempo_remanente_m1)
            self.medicos.tiempo_remanente_m1 = None

    def fin_atencion_m2(self):
        self.eventos.arrastrar_llegada_paciente()
        self.eventos.arrastrar_fin_examen()
        self.eventos.limpiar_urgente()
        atendido_suspendido = self.medicos.siguiente_m2()
        if not atendido_suspendido:
            if self.medicos.medico2_esta_ocupado():
                self.eventos.calcular_fin_atencion_m2(self.reloj)
            else:
                self.eventos.limpiar_fin_atencion_m2()
        else:
            self.eventos.calcular_fin_atencion_m2_con_remanencia(self.reloj, self.medicos.tiempo_remanente_m2)
            self.medicos.tiempo_remanente_m2 = None

    def get_table(self):
        return self.tabla


if __name__ == '__main__':
    # Hacemos que se tomen los randoms preestablecidos
    Random.debug = True
    print(Simulacion(10).get_table().to_string())
