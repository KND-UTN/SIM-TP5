from abc import ABC, abstractmethod


class Paciente:
    def __init__(self, reloj):
        self.estado = EsperaExamen()
        self.caso = SinExamenCompletado()
        self.hora_inicio_espera = reloj

    def get_fila(self):
        return [self.estado.toString(), self.caso.toString(), self.hora_inicio_espera]


# ----- ESTADOS DEL PACIENTE -----

class PacienteState(ABC):
    @abstractmethod
    def toString(self):
        pass


class EsperaExamen(PacienteState):
    def examinar(self, paciente):
        paciente.estado = SiendoExaminado()

    def toString(self):
        return 'EE'


class SiendoExaminado(PacienteState):
    def espera_comun(self, paciente):
        paciente.estado = EsperaComun()

    def espera_urgencia(self, paciente):
        paciente.estado = EsperaUrgencia()

    def atendido_comun(self, paciente):
        paciente.estado = SiendoAtendidoComun()

    def atendido_urgencia(self, paciente):
        paciente.estado = SiendoAtendidoUrgencia()

    def toString(self):
        return 'SE'


class EsperaComun(PacienteState):
    def toString(self):
        return 'EC'


class SiendoAtendidoComun(PacienteState):
    def toString(self):
        return 'SAC'


class SiendoAtendidoUrgencia(PacienteState):
    def toString(self):
        return 'SAU'


class EsperaUrgencia(PacienteState):
    def toString(self):
        return 'EU'


class Suspendido(PacienteState):
    def toString(self):
        return 'Suspendido'


# --- CASOS DEL PACIENTE ---

class PacienteCase(ABC):
    @abstractmethod
    def toString(self):
        pass


class SinExamenCompletado(PacienteCase):
    def urgencia(self, paciente):
        paciente.caso = Urgente()

    def caso_comun(self, paciente):
        paciente.caso = Comun()

    def toString(self):
        return 'SEC'


class Comun(PacienteCase):
    def toString(self):
        return 'Comun'


class Urgente(PacienteCase):
    def toString(self):
        return 'Urgente'
