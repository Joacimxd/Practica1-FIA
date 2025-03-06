import random
import time
import math
from os import system

class Mothership:
    def __init__(self, x, y):
        self.carry = []
        self.position_x = x
        self.position_y = y
    def get_x(self):
        return float(self.position_x)
    def get_y(self):
        return float(self.position_y)
    def get_carry(self):
        return self.carry
    def is_in_index(self, x, y):
        return (self.position_x, self.position_y) == (x, y)
    
class Obstacle:
    def __init__(self, n_obstacle, n):
        self.positions = self.random_positions(n_obstacle,n)
    def random_positions(self, n_obstacle, n):
        random_positions = set()
        for i in range(n_obstacle):
            random_coordinate = (random.randrange(0,n), random.randrange(0,n))
            while random_coordinate in random_positions:
                random_coordinate = (random.randrange(0,n), random.randrange(0,n))
            random_positions.add(random_coordinate)
        return random_positions
    def get_positions(self):
        return self.positions
    def is_in_index(self, x, y):
        return (x, y) in self.positions

class Agente:
    def __init__(self, x, y, n, obstacle, mothership):
        self.x = x
        self.y = y
        self.n = n
        self.obstacle = obstacle
        self.mothership = mothership
        self.carry = []
    def get_x(self):
        return float(self.x)
    def get_y(self):
        return float(self.y)
    def move(self):
        moves = []
        if not(self.mothership.is_in_index(self.get_x(), self.get_y())) and len(self.carry) > 0:
            grad1 = 1/(math.sqrt(((self.get_x()+1)-self.mothership.get_x())**2+(self.get_y()-self.mothership.get_y())**2)+1)
            grad2 = 1/(math.sqrt(((self.get_x()-1)-self.mothership.get_x())**2+(self.get_y()-self.mothership.get_y())**2)+1)
            grad3 = 1/(math.sqrt((self.get_x()-self.mothership.get_x())**2+((self.get_y()+1)-self.mothership.get_y())**2)+1)
            grad4 = 1/(math.sqrt((self.get_x()-self.mothership.get_x())**2+((self.get_y()-1)-self.mothership.get_y())**2)+1)
            if((grad1 > grad2) and not (self.obstacle.is_in_index((self.get_x())+1,self.get_y()))):
                moves.append((1, 0))
            if((grad2 > grad3) and not (self.obstacle.is_in_index((self.get_x())-1,self.get_y()))):
                moves.append((-1, 0))
            if(grad3 > grad4 and not (self.obstacle.is_in_index((self.get_x()),self.get_y()+1))):
                moves.append((0, 1))
            if(grad3 < grad4 and not (self.obstacle.is_in_index((self.get_x()),self.get_y()+1))):
                moves.append((0, -1))
        else:
            if self.get_x() > 0 and not (self.obstacle.is_in_index((self.get_x())-1,self.get_y())):
                moves.append((-1, 0))
            if self.get_x() < self.n - 1 and not (self.obstacle.is_in_index((self.get_x())+1,self.get_y())):
                moves.append((1, 0))
            if self.get_y() > 0 and not (self.obstacle.is_in_index((self.get_x()),self.get_y()-1)):
                moves.append((0, -1))
            if self.get_y() < self.n - 1 and not (self.obstacle.is_in_index((self.get_x()),self.get_y()+1)):
                moves.append((0, 1))
        if len(moves) == 0:
            if(not (self.obstacle.is_in_index((self.get_x())+1,self.get_y()))):
                moves.append((1, 0))
            if(not (self.obstacle.is_in_index((self.get_x())-1,self.get_y()))):
                moves.append((-1, 0))
            if(not (self.obstacle.is_in_index((self.get_x()),self.get_y()+1))):
                moves.append((0, 1))
            if(not (self.obstacle.is_in_index((self.get_x()),self.get_y()+1))):
                moves.append((0, -1))
            
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

class Samples:
    def __init__(self, n_samples, n, obstacle, mothership, agente):
        self.agente = agente
        self.obstacle = obstacle
        self.mothership = mothership
        self.positions = self.random_positions(n_samples,n)
    def random_positions(self, n_samples, n):
        random_positions = set()
        for _ in range(n_samples):
            random_coordinate = (random.randrange(0,n), random.randrange(0,n))
            while (random_coordinate in random_positions) or (self.obstacle.is_in_index(random_coordinate[0], random_coordinate[1])) or (self.mothership.is_in_index(random_coordinate[0], random_coordinate[1])) or (self.agente.is_in_index(random_coordinate[0], random_coordinate[1])):
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
    def __init__(self, n, number_of_samples, number_of_obstacles):
        self.n = n
        self.mothership = Mothership(5, 5)
        self.obstacle = Obstacle(number_of_obstacles, n)
        self.agente = Agente(0,0,n, self.obstacle, self.mothership)
        self.samples = Samples(number_of_samples, n, self.obstacle, self.mothership, self.agente)
    def __str__(self):
        print(self.samples.get_positions())
        sup = " " + "__" * self.n + "\n"
        lat = ""
        for i in range(self.n):
            lat += "|"
            for j in range(self.n):
                if (self.agente.is_in_index(j,i)):
                    lat += "@ "
                elif (self.mothership.is_in_index(j,i)):
                    lat += "v "
                elif (self.samples.is_in_index(j,i)):
                    lat += "& "
                elif (self.obstacle.is_in_index(j,i)):
                    lat += "# "
                else:
                    lat += "  "
            lat += "|\n"
        return sup + lat + sup + "\n" + "Bolsa del agente: " +str(self.agente.get_carry()) + "\n"
        
            
if __name__ == "__main__":
    NUMBER_OF_SAMPLES = 10
    NUMBER_OF_OBSTACLES = 10
    N = 10
    FPS = .001
    matriz = Matriz(N, NUMBER_OF_SAMPLES, NUMBER_OF_SAMPLES)
    acumShip=0
    print(matriz)
    time.sleep(FPS)
    run = True
    while run:
        if matriz.samples.is_in_index(matriz.agente.get_x(), matriz.agente.get_y()):
            matriz.agente.pick_up_sample()
            matriz.samples.delete_sample(matriz.agente.get_x(), matriz.agente.get_y())
        matriz.agente.move()
        if (matriz.mothership.is_in_index(matriz.agente.get_x(), matriz.agente.get_y())) and len(matriz.agente.carry) > 0:
            acumShip += len(matriz.agente.carry)
            matriz.agente.carry = []
        print(matriz)
        print("Bolsa de la nave: ",acumShip)
        time.sleep(FPS)
        system('clear')
        if acumShip == NUMBER_OF_OBSTACLES:
            run = False
    print("""
                                                                  
 ,-----.                        ,--.         ,--.            ,--. 
'  .--./ ,---. ,--,--,--. ,---. |  | ,---. ,-'  '-. ,---.  ,-|  | 
|  |    | .-. ||        || .-. ||  || .-. :'-.  .-'| .-. :' .-. | 
'  '--'\' '-' '|  |  |  || '-' '|  |\   --.  |  |  \   --.\ `-' | 
 `-----' `---' `--`--`--'|  |-' `--' `----'  `--'   `----' `---'  
                         `--'                                     
""")