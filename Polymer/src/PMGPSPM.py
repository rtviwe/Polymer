import os
import random
import time

import math

from Polymer.src.PMPI import pmpi_input

# Global variables
vect = 1.557  # C-C bond length
dop_radius = 1
vect_ch = 0.8  # C-H bond length
time_to_wait = 3  # lag time (seconds)

# Technical containers
c_coord_x = []
c_coord_y = []
c_coord_z = []

h_coord_x = []
h_coord_y = []
h_coord_z = []

# TODO not sure
c_in_tubes = 0
dist_btw_walls = 10


# Polyethilene generation
class Chain:

    def __init__(self, coord):
        phi = random.random()
        theta = random.random()

        self.z = vect * math.cos(2 * math.pi * theta)
        self.y = vect * math.sin(2 * math.pi * theta) * math.cos(2 * math.pi * phi)
        self.x = vect * math.sin(2 * math.pi * theta) * math.sin(2 * math.pi * phi)

        c_coord_x.extend([coord[0], coord[0] + vect / math.sqrt(2)])
        c_coord_y.extend([coord[1], coord[1] + vect / math.sqrt(2)])
        c_coord_z.extend([coord[2], coord[2]])

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
            if i2 % (bead_number + 2) != 0 and i2 % (bead_number + 2) != (bead_number + 2 - 1):
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
    f = open(os.getcwd() + str(bead_number) + '_' + str(chain_numb) + '.data', 'w')

    # Generate head of file
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


def create_tube(diameter, l, init_pos, angle_x, angle_y):
    n = round(math.pi / math.sin(r / diameter))  # number of atoms in one circle
    r2 = r / (2 * math.cos(math.pi / (2 * n)))  # auxiliary vector
    a = [[init_pos[0]], [init_pos[1] - diameter / 2], [init_pos[2]]]
    for i in range(n - 1):  # first loop
        a[0].append(round(a[0][i] - r * math.cos(math.pi * (2 * i + 1) / n), 2))
        a[1].append(round(a[1][i] + r * math.sin(math.pi * (2 * i + 1) / n), 2))
        a[2].append(round(a[2][i]))

    for k in range(int(l / tube_coeff)):  # other l loops
        if k % 4 == 2:  # (round(k%8,0) == 6) or (round(k%8,0) == 2)):
            for i in range(n):
                a[0].append(round(a[0][n * k + i] + r2 * math.cos(-math.pi / (2 * n) + 2 * math.pi * i / n), 2))
                a[1].append(round(a[1][n * k + i] - r2 * math.sin(-math.pi / (2 * n) + 2 * math.pi * i / n), 2))
                a[2].append(round(a[2][n * k + i] + 0.5 * r / math.sqrt(3), 2))

        elif k % 4 == 0:  # ((round(k%8,0) == 0) or (round(k%8,0) == 4)):
            for i in range(n):
                a[0].append(round(a[0][n * k + i] - r2 * math.cos(-math.pi / (2 * n) + 2 * math.pi * i / n), 2))
                a[1].append(round(a[1][n * k + i] + r2 * math.sin(-math.pi / (2 * n) + 2 * math.pi * i / n), 2))
                a[2].append(round(a[2][n * k + i] + 0.5 * r / math.sqrt(3), 2))

        else:  # elif((round(k%8,0) == 1) or (round(k%8,0) == 5) or (round(k%8,0) == 3) or (round(k%8,0) == 7)):
            for i in range(n):
                a[0].append(round(a[0][n * k + i], 2))
                a[1].append(round(a[1][n * k + i], 2))
                a[2].append(round(a[2][n * k + i] + r / math.sqrt(3), 2))

    a_cp = [[], [], []]

    a_cp[0] = a[0][:]
    a_cp[1] = a[1][:]
    a_cp[2] = a[2][:]

    for i in range(len(a[0])):
        a[0][i] = a_cp[0][0] + (a_cp[0][i] - a_cp[0][0]) * math.cos(angle_x) - (a_cp[2][i] - a_cp[2][0]) * \
                  math.sin(angle_x)
        a[2][i] = a_cp[2][0] + (a_cp[0][i] - a_cp[0][0]) * math.sin(angle_x) + (a_cp[2][i] - a_cp[2][0]) * \
                  math.cos(angle_x)

    a_cp[0] = a[0][:]
    a_cp[1] = a[1][:]
    a_cp[2] = a[2][:]

    for i in range(len(a[0])):
        a[1][i] = a_cp[1][0] + (a_cp[1][i] - a_cp[1][0]) * math.cos(angle_y) - (a_cp[2][i] - a_cp[2][0]) * \
                  math.sin(angle_y)
        a[2][i] = a_cp[2][0] + (a_cp[1][i] - a_cp[1][0]) * math.sin(angle_y) + (a_cp[2][i] - a_cp[2][0]) * \
                  math.cos(angle_y)

    return a


def apply_tube(diameter, l, init_pos, wall_numb, angle_x, angle_y):
    a_out = [[], [], []]

    for k in range(wall_numb):
        a_temp = create_tube(diameter - k * dist_btw_walls, l, init_pos, angle_x, angle_y)
        for i in range(len(a_out)):
            a_out[i].extend(a_temp[i])

    return a_out


def add_tube(number, l, a, n, angle_x, angle_y):
    tube_coord = tube.apply_tube(number, l, a, n, angle_x, angle_y)
    c_coord_x.extend(tube_coord[0])
    c_coord_y.extend(tube_coord[1])
    c_coord_z.extend(tube_coord[2])


def main():
    global c_in_tubes
    c_in_tubes = len(c_coord_x)

    for j in range(chain_numb):
        while 1:
            first_chain = Chain([
                random.randint(-pmpi_input.box_x / 2, pmpi_input.box_x / 2),
                random.randint(-pmpi_input.box_y / 2, pmpi_input.box_y / 2),
                random.randint(-pmpi_input.box_z / 2, pmpi_input.box_z / 2)
            ])

            chain_len = 2
            for i in range(bead_number):
                start = time.time()
                print(i, chain_len, j)

                while 1:
                    first_chain.generate()
                    if time.time() - start > time_to_wait:
                        break
                    if first_chain.check_angle() == 0 and first_chain.check_empty() == 0 and \
                            first_chain.check_border() == 0:
                        first_chain.add_bead()
                        chain_len += 1
                        break

                if time.time() - start > time_to_wait:
                    for k in range(chain_len):
                        c_coord_x.pop(-1)
                        c_coord_y.pop(-1)
                        c_coord_z.pop(-1)
                    break

            if len(c_coord_x) - c_in_tubes >= bead_number * (j + 1):
                break

    if chain_numb != 0:
        first_chain.add_hydr()

    write_in_file()


if __name__ == "__main__":
    main()
