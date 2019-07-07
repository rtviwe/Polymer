import os
import random
import time

import math

from Polymer.src.input import pmpi_input

# from input import pmpi_input

C_C_length = 1.557  # C-C длина связи
DOP_RADIUS = 1  # TODO ???
C_H_LENGTH = 0.8  # C-H длина связи
TIME_TO_WAIT = 3  # Сколько времени можно дать, чтобы искать место для новой молекулы в цепочке

# Какие-то глобальные переменные
current_x_coordinates = []
current_y_coordinates = []
current_z_coordinates = []

# TODO ???
h_coord_x = []
h_coord_y = []
h_coord_z = []

dist_btw_walls = 10  # расстояние между цепочкой и коробкой
c_in_tubes = len(current_x_coordinates)  # TODO ???


class Chain:

    # Конструктор
    def __init__(self, coord):
        current_x_coordinates.extend([coord[0], coord[0] + C_C_length / math.sqrt(2)])
        current_y_coordinates.extend([coord[1], coord[1] + C_C_length / math.sqrt(2)])
        current_z_coordinates.extend([coord[2], coord[2]])

        self.current_z = 0
        self.current_y = 0
        self.current_x = 0
        self.chain_length = 0

    # Добавляет новую молекулу в конец цепочки
    def generate(self):
        phi = random.random()
        theta = random.random()

        self.current_x = C_C_length * math.sin(2 * math.pi * theta) * math.sin(2 * math.pi * phi)
        self.current_y = C_C_length * math.sin(2 * math.pi * theta) * math.cos(2 * math.pi * phi)
        self.current_z = C_C_length * math.cos(2 * math.pi * theta)

    # Проверяет, можно ли поставить молекулу с таким углом к предыдущей
    def check_angle(self) -> bool:
        x_start = current_x_coordinates[-1]
        y_start = current_y_coordinates[-1]
        z_start = current_z_coordinates[-1]

        x_finish = current_x_coordinates[-2]
        y_finish = current_y_coordinates[-2]
        z_finish = current_z_coordinates[-2]

        cos_angle = ((x_start - x_finish) * self.current_x + (y_start - y_finish) * self.current_y + (
                z_start - z_finish) * self.current_z) / C_C_length ** 2
        if 0.25 < cos_angle < 0.55:
            return True
        else:
            return False

    # Получает количество соседей
    def get_neighbor_count(self):
        neighbor_count = 0
        for i in range(len(current_x_coordinates) - 1):
            dist = math.sqrt(
                (current_x_coordinates[i] - (self.current_x + current_x_coordinates[-1])) ** 2 + (
                        current_y_coordinates[i] - (self.current_y + current_y_coordinates[-1])) ** 2 + (
                        current_z_coordinates[i] - (self.current_z + current_z_coordinates[-1])) ** 2)

            if dist < C_C_length + DOP_RADIUS:
                neighbor_count += 1

        return neighbor_count

    # Проверяет не зашли ли за границу коробки
    def check_border(self) -> bool:
        if (abs(current_x_coordinates[-1] + self.current_x) < pmpi_input.box_x / 2 and
                abs(current_y_coordinates[-1] + self.current_y) < pmpi_input.box_y / 2 and
                abs(current_z_coordinates[-1] + self.current_z) < pmpi_input.box_z / 2):
            return True
        else:
            return False

    # Добавляет молекулу на конец цепочки
    def add_bead(self):
        current_x_coordinates.append(current_x_coordinates[-1] + self.current_x)
        current_y_coordinates.append(current_y_coordinates[-1] + self.current_y)
        current_z_coordinates.append(current_z_coordinates[-1] + self.current_z)

    # TODO что это
    def add_hydr(self):
        for i2 in range(len(current_x_coordinates) - c_in_tubes):
            i = i2 + c_in_tubes
            if i2 % (pmpi_input.bead_number + 2) != 0 and i2 % (pmpi_input.bead_number + 2) != \
                    (pmpi_input.bead_number + 2 - 1):
                a_x = (current_x_coordinates[i + 1] - current_x_coordinates[i]) / C_C_length
                a_y = (current_y_coordinates[i + 1] - current_y_coordinates[i]) / C_C_length
                a_z = (current_z_coordinates[i + 1] - current_z_coordinates[i]) / C_C_length

                b_x = (current_x_coordinates[i - 1] - current_x_coordinates[i]) / C_C_length
                b_y = (current_y_coordinates[i - 1] - current_y_coordinates[i]) / C_C_length
                b_z = (current_z_coordinates[i - 1] - current_z_coordinates[i]) / C_C_length

                sin_angle = math.sqrt(1 - (a_x * b_x + a_y * b_y + a_z * b_z) ** 2)

                c_x = (a_y * b_z - a_z * b_y) / sin_angle
                c_y = (a_z * b_x - a_x * b_z) / sin_angle
                c_z = (a_x * b_y - a_y * b_x) / sin_angle

                h_coord_x.append(current_x_coordinates[i] + c_x * C_H_LENGTH)
                h_coord_y.append(current_y_coordinates[i] + c_y * C_H_LENGTH)
                h_coord_z.append(current_z_coordinates[i] + c_z * C_H_LENGTH)

                h_coord_x.append(current_x_coordinates[i] - c_x * C_H_LENGTH)
                h_coord_y.append(current_y_coordinates[i] - c_y * C_H_LENGTH)
                h_coord_z.append(current_z_coordinates[i] - c_z * C_H_LENGTH)


# Записывает цепочку в файл srcN_M.data
def write_in_file():
    f = open(os.getcwd() + str(pmpi_input.bead_number) + '_' + str(pmpi_input.chain_number) + '.data', 'w')

    f.write('\n' + str(len(current_x_coordinates) + len(h_coord_x)) + ' atoms' + '\n')
    f.write('2 atom types' + '\n' + '\n')
    f.write(str(-pmpi_input.box_x / 2 - 1) + ' ' + str(pmpi_input.box_x / 2 + 1) + ' xlo xhi' + '\n')
    f.write(str(-pmpi_input.box_y / 2 - 1) + ' ' + str(pmpi_input.box_y / 2 + 1) + ' ylo yhi' + '\n')
    f.write(str(-pmpi_input.box_z / 2 - 1) + ' ' + str(pmpi_input.box_z / 2 + 1) + ' zlo zhi' + '\n' + '\n')
    f.write('Masses' + '\n' + '\n' + '1 12.0' + '\n' + '2 1.0' + '\n' + '\n' 'Atoms' + '\n' + '\n')

    for i in range(len(current_x_coordinates)):
        f.write(
            str(i + 1) + ' ' + '1 ' + str(current_x_coordinates[i]) + ' ' + str(current_y_coordinates[i]) + ' ' + str(
                current_z_coordinates[i]) + '\n')
    for i in range(len(h_coord_x)):
        f.write(str(i + 1 + len(current_x_coordinates)) + ' ' + '2 ' + str(h_coord_x[i]) + ' ' + str(
            h_coord_y[i]) + ' ' + str(
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
    current_x_coordinates.extend(tube_coord[0])
    current_y_coordinates.extend(tube_coord[1])
    current_z_coordinates.extend(tube_coord[2])


def main():
    global c_in_tubes
    global current_x_coordinates, current_y_coordinates, current_z_coordinates
    c_in_tubes = len(current_x_coordinates)

    for j in range(pmpi_input.chain_number):
        while 1:
            current_chain = Chain([
                random.randint(-pmpi_input.box_x / 2, pmpi_input.box_x / 2),
                random.randint(-pmpi_input.box_y / 2, pmpi_input.box_y / 2),
                random.randint(-pmpi_input.box_z / 2, pmpi_input.box_z / 2)
            ])

            for i in range(pmpi_input.bead_number):
                start = time.time()
                print(i, current_chain.chain_length, j)

                while 1:
                    current_chain.generate()
                    if time.time() - start > TIME_TO_WAIT:
                        break

                    if current_chain.check_angle() and current_chain.get_neighbor_count() == 0 \
                            and current_chain.check_border():
                        current_chain.add_bead()
                        current_chain.chain_length += 1
                        break

                # if time.time() - start > TIME_TO_WAIT:
                #     for k in range(current_chain.chain_length):
                #         current_x_coordinates.pop(-1)
                #         current_y_coordinates.pop(-1)
                #         current_z_coordinates.pop(-1)
                #     break

                # иногда закомментированный код сверху падает, это альтернатива, надо проверить
                if time.time() - start > TIME_TO_WAIT:
                    current_x_coordinates = []
                    current_y_coordinates = []
                    current_z_coordinates = []
                    break

            from Polymer.src.output import plot_chain_with_args
            # from output import plot_chain_with_args
            plot_chain_with_args((pmpi_input.bead_number, c_in_tubes, current_x_coordinates, current_y_coordinates,
                                  current_z_coordinates))

            if len(current_x_coordinates) - c_in_tubes >= pmpi_input.bead_number * (j + 1):
                break

    if pmpi_input.chain_number != 0:
        current_chain.add_hydr()

    write_in_file()


# Вот тут надо запускать
if __name__ == "__main__":
    main()
