
import random
import time
from os import system

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
            moves.append((-50, 0))
        if self.get_x() < self.n - 1:
            moves.append((50, 0))
        if self.get_y() > 0:
            moves.append((0, -50))
        if self.get_y() < self.n - 1:
            moves.append((0, 50))
        random_choice = random.choice(moves)
        self.x += random_choice[0]
        self.y += random_choice[1]
        return random_choice[0], random_choice[1]
    
    def pick_up_sample(self):
        self.carry.append("&")
    def get_carry(self):
        return self.carry
    def carrying_samples(self):
        return len(self.carry) > 0
    def is_in_index(self, x, y):
        return self.x == x and self.y == y

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
        
            
if __name__ == "__main__":
    agente = Agente(0,0,10)
    samples = Samples(10, 10)
    mothership = Mothership(5, 5)
    matriz = Matriz(10, agente, samples, mothership)
    print(matriz)
    time.sleep(.3)
    for i in range(1000):
        matriz.agente.move()
        if matriz.samples.is_in_index(matriz.agente.get_x(), matriz.agente.get_y()):
            matriz.agente.pick_up_sample()
            matriz.samples.delete_sample(matriz.agente.get_x(), matriz.agente.get_y())
        print(matriz)
        time.sleep(.1) 
        system('clear') 
