import pygame
import random
import math
import time

color = (0, 0, 0)
radius = 15
n = 75
tolerance = 0.1
atime = 0
distance_traveled = 0
distance_between_impacts = []
number_of_atoms = 40
(width, height) = (800, 800)
tps_max = 200
tps_clock = pygame.time.Clock()
tps_delta = 0.0
timer = time.time()
pomiar1 = []
pomiar2 = []

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zadanie programistyczne wariant B")
screen.fill(color)


def hit(object1, object2):
    global distance_traveled
    dx = object1.x - object2.x
    dy = object1.y - object2.y
    distances = math.hypot(dx, dy) - tolerance * radius

    if distances <= 2 * radius:

        if object1.color == (200, 0, 0):
            distance_between_impacts.append(round(distance_traveled, 2))
            distance_traveled = 0
        object1.y = height - object1.y
        object2.y = height - object2.y
        collision_point = ((object1.x + object2.x) / 2, (object1.y + object2.y) / 2)

        # wyznaczenie współczynników a oraz b prostej równoległej
        ar = (object1.y - object2.y) / (object1.x - object2.x)
        br = object1.y - (object1.y - object2.y) / (object1.x - object2.x) * object1.x

        # wyznaczenie współczynnika a prostej prostopadłej
        ap = -1 / ar

        # wyznaczenie współczynnika b prostej prostopadłej atomu 1
        bp1 = object1.y - ap * object1.x

        # wyznaczenie współczynnika b prostej prostopadłej atomu 2
        bp2 = object2.y - ap * object2.x

        # wyznaczenie wektora równoległego atomu 1
        new_br1 = (object1.y + object1.speed_y) - ar * (object1.x + object1.speed_x)
        # punkt przecięcia prostych {y1 = ap * x1 + bp1} oraz {y1 = ar * x1 + new_br1}
        x1 = (bp1 - new_br1) / (ar - ap)
        y1 = ap * x1 + bp1
        V_r1 = ((object1.x + object1.speed_x) - x1, (object1.y + object1.speed_y) - y1)

        # wyznaczenie wektora równoległego atomu 2
        new_br2 = (object2.y + object2.speed_y) - ar * (object2.x + object2.speed_x)
        # punkt przecięcia prostych {yp2 = ap * xp2 + bp2} oraz {yp2 = ar * xp2 + new_br2}
        xp2 = (bp2 - new_br2) / (ar - ap)
        yp2 = ap * xp2 + bp2
        V_r2 = ((object2.x + object2.speed_x) - xp2, (object2.y + object2.speed_y) - yp2)

        # wyznaczenie wektora prostopadłego atomu 1
        new_bp1 = (object1.y + object1.speed_y) - ap * (object1.x + object1.speed_x)
        # punkt przecięcia prostych {yr1 = ar * xr1 + br} oraz {yr1 = ap * xr1 + new_bp1}
        xr1 = (br - new_bp1) / (ap - ar)
        yr1 = ar * xr1 + br
        V_p1 = ((object1.x + object1.speed_x) - xr1, (object1.y + object1.speed_y) - yr1)

        # wyznaczenie wektora prostopadłego atomu 2
        new_bp2 = (object2.y + object2.speed_y) - ap * (object2.x + object2.speed_x)
        # punkt przecięcia prostych {yr2 = ar * xr2 + br} oraz {yr2 = ap * xr2 + new_bp2}
        xr2 = (br - new_bp2) / (ap - ar)
        yr2 = ar * xr2 + br
        V_p2 = ((object2.x + object2.speed_x) - xr2, (object2.y + object2.speed_y) - yr2)

        object1.speed_x, object1.speed_y = V_p1[0] + V_r2[0], V_p1[1] + V_r2[1]
        object2.speed_x, object2.speed_y = V_p2[0] + V_r1[0], V_p2[1] + V_r1[1]

        object1.y = height - object1.y
        object2.y = height - object2.y


class Atom(object):
    def __init__(self, position, size, color):
        self.x, self.y = position
        self.size = size
        self.color = color
        self.speed_x, self.speed_y = random.uniform(-1, 1), random.uniform(-1, 1)

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.size)

    def move(self):
        self.x += self.speed_x
        self.y -= self.speed_y

    def hit_wall(self):
        if self.x + self.size > width:
            self.x = 2 * (width - self.size) - self.x
            self.speed_x = -self.speed_x
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.speed_x = -self.speed_x

        if self.y + self.size > height:
            self.y = 2 * (height - self.size) - self.y
            self.speed_y = -self.speed_y
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.speed_y = -self.speed_y


def position_generation():
    def same_position(coord1, coord2):
        dx = coord1[0] - coord2[0]
        dy = coord1[1] - coord2[1]
        distance = math.hypot(dx, dy)
        if distance <= 3 * radius:
            return True
        else:
            return False

    atoms_list = []
    atoms_positions = []
    atom = Atom((radius, height - radius), radius, (200, 0, 0))
    atoms_list.append(atom)
    atoms_positions.append((radius, height - radius))
    quantity = 1
    attempt = 0
    while quantity < number_of_atoms:
        unique = True
        coordinates = (random.randint(radius, width - radius), random.randint(radius, height - radius))
        attempt += 1

        for i in atoms_positions:
            if same_position(coordinates, i) == True:
                unique = False
        if unique == True:
            attempt = 0
            atoms_positions.append(coordinates)
            atom2 = Atom(coordinates, radius, (0, 0, 200))
            atoms_list.append(atom2)
            quantity += 1
        elif attempt >= 50000:
            print("Nie można wygenerować podanej liczby atomów! Liczba wygenerowanych atomów: ", quantity)
            return atoms_list
    return atoms_list


lista = position_generation()

set = True
while (set):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            set = False
    if (round(atime, 2) == 30 and len(pomiar1) == 0) or (round(atime, 2) == 150 and len(pomiar1) == 1):
        pomiar2.append(len(distance_between_impacts))

        if len(distance_between_impacts) == 0:
            mean_free_path = distance_traveled
        else:
            mean_free_path = round((sum(distance_between_impacts)) / (len(distance_between_impacts)), 2)
        pomiar1.append(mean_free_path)

    elif atime >= 300:
        pomiar2.append(len(distance_between_impacts))
        if len(distance_between_impacts) == 0:
            mean_free_path = distance_traveled
        else:
            mean_free_path = round((sum(distance_between_impacts)) / (len(distance_between_impacts)), 2)
        pomiar1.append(mean_free_path)
        set = False

    screen.fill(color)

    for atoms in lista:
        atoms.display()
    tps_delta += tps_clock.tick() / 1000

    while tps_delta > 1 / tps_max:
        atime += 1 / tps_max
        tps_delta -= 1 / tps_max
        for i, atoms in enumerate(lista):
            atoms.move()
            atoms.hit_wall()
            if atoms.color == (200, 0, 0):
                distance_traveled += abs(atoms.speed_x) + abs(atoms.speed_y)
            for atoms2 in lista[i + 1:]:
                hit(atoms, atoms2)

    pygame.display.flip()

if len(distance_between_impacts) == 0:
    mean_free_path = distance_traveled
else:
    mean_free_path = round((sum(distance_between_impacts)) / (len(distance_between_impacts)), 2)
print("POMIAR:")
print("Liczba atomów: ", number_of_atoms)
print("Średnia droga swobodna atomu czerwonego = ", mean_free_path)
print("Liczba zderzeń atomu czerwonego = ", len(distance_between_impacts))
print("Pomiary drogi: ", *pomiar1)
print("Pomiary zderzeń: ", *pomiar2)
print("Czas: ", atime)
print(time.time() - timer)