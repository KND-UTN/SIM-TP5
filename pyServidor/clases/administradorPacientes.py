from .paciente import Paciente


class AdministradorPacientes:
    def __init__(self):
        self.pacientes = {}
        self.last_id = 0

    def nuevo_paciente(self, reloj):
        nuevoPaciente = Paciente(reloj)
        self.pacientes[self.last_id] = nuevoPaciente
        self.last_id += 1
        return nuevoPaciente

    def get_fila(self):
        fila = []
        for id_paciente in self.pacientes:
            fila += self.pacientes[id_paciente].get_fila()
        return fila
