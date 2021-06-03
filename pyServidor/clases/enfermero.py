from abc import ABC, abstractmethod


class Enfermero:

    def __init__(self):
        self.estado: EnfermeroState = Libre()
        self.cola = []
        self.paciente_actual = None

    def add_paciente(self, paciente):
        if isinstance(self.estado, Libre):
            self.paciente_actual = paciente
            self.paciente_actual.estado.examinar(self.paciente_actual)
            self.estado = Ocupado()
            return 1    # Fue atendido en el momento

        self.cola.append(paciente)
        return 0    # Fue añadido a la cola

    def atender_siguiente(self):
        anterior = self.paciente_actual
        if len(self.cola) > 0:
            self.paciente_actual = self.cola.pop(0)
            self.paciente_actual.estado.examinar(self.paciente_actual)
        else:
            self.estado = Libre()
        return anterior

    def esta_ocupado(self):
        return isinstance(self.estado, Ocupado)


    def get_fila(self):
        if self.esta_ocupado():
            return [self.estado.toString() + " (P" + str(self.paciente_actual.id) + ")", len(self.cola)]
        return [self.estado.toString(), len(self.cola)]


class EnfermeroState(ABC):
    @abstractmethod
    def toString(self):
        pass


class Ocupado(EnfermeroState):
    def toString(self):
        return 'Ocupado'


class Libre(EnfermeroState):
    def toString(self):
        return 'Libre'