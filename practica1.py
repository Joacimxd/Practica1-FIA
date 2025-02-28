#Librerias
import random
import time
from os import system

# Clase de la nave nodriza
# Atributos: lo que el agente ha dejado, la posicion en x y la posicion en y
# Metodos: obtener la posicion en x, obtener la posicion en y, obtener lo que lleva, si esta en la posicion x y y
class Mothership:
    def __init__(self, x, y):
        self.carry = []
        self.position_x = x
        self.position_y = y
    def get_x(self):
        return self.position_x
    def get_y(self):    
        return self.position_y
    def get_carry(self):
        return self.carry
    def is_in_index(self, x, y):
        return (self.position_x, self.position_y) == (x, y)

# Clase del agente
# Atributos: la posicion en x, la posicion en y, el tamaño de la matriz y lo que lleva
# Metodos: obtener la posicion en x, obtener la posicion en y, moverse aleatoriamente, recoger una muestra, obtener lo que lleva, si lleva algo, si esta en la posicion x y y
class Agente:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        self.carry = []
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def move(self):
        moves = []
        if self.get_x() > 0:
            moves.append((-1, 0))
        if self.get_x() < self.n - 1:
            moves.append((1, 0))
        if self.get_y() > 0:
            moves.append((0, -1))
        if self.get_y() < self.n - 1:
            moves.append((0, 1))
        random_choice = random.choice(moves)
        self.x += random_choice[0]
        self.y += random_choice[1]
    def pick_up_sample(self):
        self.carry.append("&")
    def get_carry(self):
        return self.carry
    def carrying_samples(self):
        return len(self.carry) > 0
    def is_in_index(self, x, y):
        return self.x == x and self.y == y

# Clase de las muestras
# Atributos: las posiciones de las muestras
# Metodos: obtener las posiciones, eliminar una muestra, si esta en la posicion x y y
class Samples:
    def __init__(self, n_samples, n):
        self.positions = self.random_positions(n_samples,n)
    def random_positions(self, n_samples, n):
        random_positions = set()
        for i in range(n_samples):
            random_coordinate = (random.randrange(0,n), random.randrange(0,n))
            while random_coordinate in random_positions:
                random_coordinate = (random.randrange(0,n), random.randrange(0,n))
            random_positions.add(random_coordinate)
        return random_positions
    def get_positions(self):
        return self.positions
    def delete_sample(self, x, y):
        self.positions.remove((x, y))
    def is_in_index(self, x, y):
        return (x, y) in self.positions

# Clase de la matriz
# Atributos: el tamaño de la matriz, el agente, las muestras y la nave nodriza
# Metodos: obtener la matriz en forma de string
class Matriz:
    def __init__(self, n, agente, samples, mothership):
        self.n = n
        self.agente = agente
        self.samples = samples
        self.mothership = mothership
    def __str__(self):
        sup = " " + "__" * self.n + "\n"
        lat = ""
        for i in range(self.n):
            lat += "|"
            for j in range(self.n):
                if (self.agente.is_in_index(j,i)):
                    lat += "@ "
                elif (self.samples.is_in_index(j,i)):
                    lat += "& "
                elif (self.mothership.is_in_index(j,i)):
                    lat += "v "
                else:
                    lat += "  "
            lat += "|\n"
        return sup + lat + sup + "\n" + str(self.agente.get_carry()) + "\n"
        
            
#Aqui esta la logica principal del programa (main)
if __name__ == "__main__":
    agente = Agente(0,0,10)#Un agente en la posicion (0,0) de una matriz de 10x10
    samples = Samples(10, 10)#10 muestras en una matriz de 10x10
    mothership = Mothership(5, 5)#Una nave nodriza en la posicion (5,5)
    matriz = Matriz(10, agente, samples, mothership)#Una matriz de 10x10 con un agente, muestras y una nave nodriza
    print(matriz)
    time.sleep(.3)
    for i in range(1000):
        matriz.agente.move()
        #Si el agente esta en la posicion de una muestra la recoge y la borra de la lista de muestras
        if matriz.samples.is_in_index(matriz.agente.get_x(), matriz.agente.get_y()):
            matriz.agente.pick_up_sample()
            matriz.samples.delete_sample(matriz.agente.get_x(), matriz.agente.get_y())
        print(matriz)
        time.sleep(.1) #Espera de 0.1 segundos para ser perceptible
        system('clear') #Borra la pantalla de la terminal

#Por hacer:
#Implementar la clase obstaculos.
#Implementar el metodo __str__ de la matriz con obstaculos.
#Implementar en el metodo move de la clase agenente la logica para evitar obstaculos y 
#regresar a la nave nodriza con la ecuacion.
#Implementar la logica para dejar las muestras en la nave.