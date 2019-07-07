import os
import random
import time

import math

from Polymer.src.input import pmpi_input

# from input import pmpi_input

# Какие-то глобальные переменные
vect = 1.557  # C-C bond length
dop_radius = 1
vect_ch = 0.8  # C-H bond length
time_to_wait = 3  # lag time (seconds)

c_coord_x = []
c_coord_y = []
c_coord_z = []

h_coord_x = []
h_coord_y = []
h_coord_z = []

# TODO not sure
dist_btw_walls = 10
c_in_tubes = len(c_coord_x)


# Цепочка полиэтилена
class Chain:

    def __init__(self, coord):
        c_coord_x.extend([coord[0], coord[0] + vect / math.sqrt(2)])
        c_coord_y.extend([coord[1], coord[1] + vect / math.sqrt(2)])
        c_coord_z.extend([coord[2], coord[2]])

        self.z = 0
        self.y = 0
        self.x = 0

    def generate(self):
        phi = random.random()
        theta = random.random()

        self.x = vect * math.sin(2 * math.pi * theta) * math.sin(2 * math.pi * phi)
        self.y = vect * math.sin(2 * math.pi * theta) * math.cos(2 * math.pi * phi)
        self.z = vect * math.cos(2 * math.pi * theta)

    def check_angle(self):
        x_beg = c_coord_x[-1]
        y_beg = c_coord_y[-1]
        z_beg = c_coord_z[-1]

        x_end = c_coord_x[-2]
        y_end = c_coord_y[-2]
        z_end = c_coord_z[-2]

        cos_angle = ((x_beg - x_end) * self.x + (y_beg - y_end) * self.y + (z_beg - z_end) * self.z) / vect ** 2
        if 0.25 < cos_angle < 0.55:
            return 0
        else:
            return 1

    def check_empty(self):
        neighbor_count = 0
        for i in range(len(c_coord_x) - 1):
            dist = math.sqrt(
                (c_coord_x[i] - (self.x + c_coord_x[-1])) ** 2 + (c_coord_y[i] - (self.y + c_coord_y[-1])) ** 2 + (
                        c_coord_z[i] - (self.z + c_coord_z[-1])) ** 2)

            if dist < vect + dop_radius:
                neighbor_count += 1

        return neighbor_count

    def check_border(self):
        if (abs(c_coord_x[-1] + self.x) < pmpi_input.box_x / 2 and
                abs(c_coord_y[-1] + self.y) < pmpi_input.box_y / 2 and
                abs(c_coord_z[-1] + self.z) < pmpi_input.box_z / 2):
            return 0
        else:
            return 1

    def add_bead(self):
        c_coord_x.append(c_coord_x[-1] + self.x)
        c_coord_y.append(c_coord_y[-1] + self.y)
        c_coord_z.append(c_coord_z[-1] + self.z)

    def add_hydr(self):
        for i2 in range(len(c_coord_x) - c_in_tubes):
            i = i2 + c_in_tubes
            if i2 % (pmpi_input.bead_number + 2) != 0 and i2 % (pmpi_input.bead_number + 2) != \
                    (pmpi_input.bead_number + 2 - 1):
                a_x = (c_coord_x[i + 1] - c_coord_x[i]) / vect
                a_y = (c_coord_y[i + 1] - c_coord_y[i]) / vect
                a_z = (c_coord_z[i + 1] - c_coord_z[i]) / vect

                b_x = (c_coord_x[i - 1] - c_coord_x[i]) / vect
                b_y = (c_coord_y[i - 1] - c_coord_y[i]) / vect
                b_z = (c_coord_z[i - 1] - c_coord_z[i]) / vect

                sin_angle = math.sqrt(1 - (a_x * b_x + a_y * b_y + a_z * b_z) ** 2)

                c_x = (a_y * b_z - a_z * b_y) / sin_angle
                c_y = (a_z * b_x - a_x * b_z) / sin_angle
                c_z = (a_x * b_y - a_y * b_x) / sin_angle

                h_coord_x.append(c_coord_x[i] + c_x * vect_ch)
                h_coord_y.append(c_coord_y[i] + c_y * vect_ch)
                h_coord_z.append(c_coord_z[i] + c_z * vect_ch)

                h_coord_x.append(c_coord_x[i] - c_x * vect_ch)
                h_coord_y.append(c_coord_y[i] - c_y * vect_ch)
                h_coord_z.append(c_coord_z[i] - c_z * vect_ch)


def write_in_file():
    f = open(os.getcwd() + str(pmpi_input.bead_number) + '_' + str(pmpi_input.chain_number) + '.data', 'w')

    f.write('\n' + str(len(c_coord_x) + len(h_coord_x)) + ' atoms' + '\n')
    f.write('2 atom types' + '\n' + '\n')
    f.write(str(-pmpi_input.box_x / 2 - 1) + ' ' + str(pmpi_input.box_x / 2 + 1) + ' xlo xhi' + '\n')
    f.write(str(-pmpi_input.box_y / 2 - 1) + ' ' + str(pmpi_input.box_y / 2 + 1) + ' ylo yhi' + '\n')
    f.write(str(-pmpi_input.box_z / 2 - 1) + ' ' + str(pmpi_input.box_z / 2 + 1) + ' zlo zhi' + '\n' + '\n')
    f.write('Masses' + '\n' + '\n' + '1 12.0' + '\n' + '2 1.0' + '\n' + '\n' 'Atoms' + '\n' + '\n')

    for i in range(len(c_coord_x)):
        f.write(str(i + 1) + ' ' + '1 ' + str(c_coord_x[i]) + ' ' + str(c_coord_y[i]) + ' ' + str(c_coord_z[i]) + '\n')
    for i in range(len(h_coord_x)):
        f.write(str(i + 1 + len(c_coord_x)) + ' ' + '2 ' + str(h_coord_x[i]) + ' ' + str(h_coord_y[i]) + ' ' + str(
            h_coord_z[i]) + '\n')

    f.close()


def create_tube(diameter, circle_length, initial_position, angle_x, angle_y):
    n = round(math.pi / math.sin(pmpi_input.r / diameter))  # number of atoms in one circle
    r2 = pmpi_input.r / (2 * math.cos(math.pi / (2 * n)))  # auxiliary vector
    tube = [[initial_position[0]], [initial_position[1] - diameter / 2], [initial_position[2]]]

    for i in range(n - 1):  # first loop
        tube[0].append(round(tube[0][i] - pmpi_input.r * math.cos(math.pi * (2 * i + 1) / n), 2))
        tube[1].append(round(tube[1][i] + pmpi_input.r * math.sin(math.pi * (2 * i + 1) / n), 2))
        tube[2].append(round(tube[2][i]))

    for k in range(int(circle_length / pmpi_input.tube_coeff)):  # other l loops
        if k % 4 == 2:  # (round(k%8,0) == 6) or (round(k%8,0) == 2)):
            for i in range(n):
                tube[0].append(round(tube[0][n * k + i] + r2 * math.cos(-math.pi / (2 * n) + 2 * math.pi * i / n), 2))
                tube[1].append(round(tube[1][n * k + i] - r2 * math.sin(-math.pi / (2 * n) + 2 * math.pi * i / n), 2))
                tube[2].append(round(tube[2][n * k + i] + 0.5 * pmpi_input.r / math.sqrt(3), 2))

        elif k % 4 == 0:  # ((round(k%8,0) == 0) or (round(k%8,0) == 4)):
            for i in range(n):
                tube[0].append(round(tube[0][n * k + i] - r2 * math.cos(-math.pi / (2 * n) + 2 * math.pi * i / n), 2))
                tube[1].append(round(tube[1][n * k + i] + r2 * math.sin(-math.pi / (2 * n) + 2 * math.pi * i / n), 2))
                tube[2].append(round(tube[2][n * k + i] + 0.5 * pmpi_input.r / math.sqrt(3), 2))

        else:  # elif((round(k%8,0) == 1) or (round(k%8,0) == 5) or (round(k%8,0) == 3) or (round(k%8,0) == 7)):
            for i in range(n):
                tube[0].append(round(tube[0][n * k + i], 2))
                tube[1].append(round(tube[1][n * k + i], 2))
                tube[2].append(round(tube[2][n * k + i] + pmpi_input.r / math.sqrt(3), 2))

    temp_tube = [[], [], []]

    temp_tube[0] = tube[0][:]
    temp_tube[1] = tube[1][:]
    temp_tube[2] = tube[2][:]

    for i in range(len(tube[0])):
        tube[0][i] = temp_tube[0][0] + (temp_tube[0][i] - temp_tube[0][0]) * math.cos(angle_x) - (
                temp_tube[2][i] - temp_tube[2][0]) * math.sin(angle_x)
        tube[2][i] = temp_tube[2][0] + (temp_tube[0][i] - temp_tube[0][0]) * math.sin(angle_x) + (
                temp_tube[2][i] - temp_tube[2][0]) * math.cos(angle_x)

    temp_tube[0] = tube[0][:]
    temp_tube[1] = tube[1][:]
    temp_tube[2] = tube[2][:]

    for i in range(len(tube[0])):
        tube[1][i] = temp_tube[1][0] + (temp_tube[1][i] - temp_tube[1][0]) * math.cos(angle_y) - (
                temp_tube[2][i] - temp_tube[2][0]) * math.sin(angle_y)
        tube[2][i] = temp_tube[2][0] + (temp_tube[1][i] - temp_tube[1][0]) * math.sin(angle_y) + (
                temp_tube[2][i] - temp_tube[2][0]) * math.cos(angle_y)

    return tube


def apply_tube(diameter, circle_length, initial_position, wall_number, angle_x, angle_y):
    a_out = [[], [], []]

    for k in range(wall_number):
        a_temp = create_tube(diameter - k * dist_btw_walls, circle_length, initial_position, angle_x, angle_y)
        for i in range(len(a_out)):
            a_out[i].extend(a_temp[i])

    return a_out


def add_tube(number, circle_length, initial_position, wall_number, angle_x, angle_y):
    tube_coord = apply_tube(number, circle_length, initial_position, wall_number, angle_x, angle_y)
    c_coord_x.extend(tube_coord[0])
    c_coord_y.extend(tube_coord[1])
    c_coord_z.extend(tube_coord[2])


def main():
    global c_in_tubes
    c_in_tubes = len(c_coord_x)

    for j in range(pmpi_input.chain_number):
        while 1:
            first_chain = Chain([
                random.randint(-pmpi_input.box_x / 2, pmpi_input.box_x / 2),
                random.randint(-pmpi_input.box_y / 2, pmpi_input.box_y / 2),
                random.randint(-pmpi_input.box_z / 2, pmpi_input.box_z / 2)
            ])

            for i in range(pmpi_input.bead_number):
                start = time.time()
                print(i, pmpi_input.chain_length, j)

                while 1:
                    first_chain.generate()
                    if time.time() - start > time_to_wait:
                        break
                    if first_chain.check_angle() == 0 and first_chain.check_empty() == 0 and \
                            first_chain.check_border() == 0:
                        first_chain.add_bead()
                        pmpi_input.chain_length += 1
                        break

                if time.time() - start > time_to_wait:
                    for k in range(pmpi_input.chain_length):
                        c_coord_x.pop(-1)
                        c_coord_y.pop(-1)
                        c_coord_z.pop(-1)
                    break

            from Polymer.src.output import plot_chain_with_args
            # from Polymer.src.output import plot_chain_with_args
            plot_chain_with_args((pmpi_input.bead_number, c_in_tubes, c_coord_x, c_coord_y, c_coord_z))

            if len(c_coord_x) - c_in_tubes >= pmpi_input.bead_number * (j + 1):
                break

    if pmpi_input.chain_number != 0:
        first_chain.add_hydr()

    write_in_file()


# Вот тут надо запускать
if __name__ == "__main__":
    main()
