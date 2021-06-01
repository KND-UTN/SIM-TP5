from random import Random as RandomOriginal

# Clase estatica de numeros randoms para facilitar el Debug
class Random:
    debug = False
    debug_random_llegada = [0.39439, 0.65166, 0.22142, 0.69935, 0.60495, 0.19115, 0.72302, 0.60205, 0.60524, 0.73539, 0.40682]
    debug_random_examen = [0.05442, 0.40143, 0.86187, 0.09395, 0.81688, 0.90532, 0.52605, 0.96621, 0.76731, 0.75220, 0.66889]
    debug_random_caso = [0.93197, 0.12518, 0.90833, 0.38340, 0.60171, 0.13047, 0.28361, 0.77239, 0.86874, 0.82197, 0.86237]
    debug_random_atencion = [0.95606, 0.18350, 0.97066, 0.05682, 0.58252, 0.17617, 0.51508, 0.31297, 0.79248, 0.57154, 0.16576]

    @staticmethod
    def randomLlegada():
        if Random.debug:
            return Random.debug_random_llegada.pop(0)
        else:
            return RandomOriginal().random()

    @staticmethod
    def randomExamen():
        if Random.debug:
            return Random.debug_random_examen.pop(0)
        else:
            return RandomOriginal().random()

    @staticmethod
    def randomCaso():
        if Random.debug:
            return Random.debug_random_caso.pop(0)
        else:
            return RandomOriginal().random()

    @staticmethod
    def randomAtencion():
        if Random.debug:
            return Random.debug_random_atencion.pop(0)
        else:
            return RandomOriginal().random()
