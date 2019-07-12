import os
import random

import math
import pylab
from mpl_toolkits.mplot3d import Axes3D

from src.bead import Bead
from src.input import polymer_input

C_C_length = 1.557  # длина C-C связи
DOP_RADIUS = 1  # дополнительный радиус, чтобы не вставлять молекулу впритык к другим
C_H_LENGTH = 0.8  # длина C-H связи
WALL_PADDING = 10  # расстояние между цепочкой и коробкой
C_IN_TUBES = 0  # TODO ???
current_chain_id = 0  # костыль, чтобы делать айдишники от 0 до N для цепей


class Chain:
    color = ['red', 'green', 'blue', 'yellow', 'black', 'pink']

    # Конструктор
    def __init__(self, beads: [Bead]):
        global current_chain_id
        self.id = current_chain_id
        current_chain_id += 1

        self.beads: [Bead] = beads
        self.chain_length: int = len(beads)
        self.hydrogen: [Bead] = []

    # Добавляет молекулу в цепь
    def add_bead(self, bead: Bead):
        self.beads.append(bead)
        self.chain_length += 1

    # Создает новую молекулу
    # TODO можно сразу генерировать в нужном месте, чтобы потом не проверять и заново генерировать
    def generate(self) -> Bead:
        maxLen = round(C_C_length + 2 * polymer_input.r)
        x: float = random.randint(self.beads[-1].x - maxLen,
                                  self.beads[-1].x + maxLen)
        maxLen = round(math.sqrt(round(C_C_length + 2 * polymer_input.r) ** 2 - (x - self.beads[-1].x) ** 2))
        y: float = random.randint(self.beads[-1].y - maxLen,
                                  self.beads[-1].y + maxLen)
        kostyl = round(C_C_length + 2 * polymer_input.r) ** 2 - (x - self.beads[-1].x) ** 2 - (y - self.beads[-1].y) ** 2
        if kostyl < 0:
            kostyl += 1
        z: float = round(math.sqrt(round(kostyl)) + self.beads[-1].z)

        return Bead(x, y, z)

    # TODO сделать проверку соседей не только для текущей цепи, а для всех уже построенных
    # Проверяет, можно ли поставить молекулу с таким углом к двум предыдущим

    def check_angle(self, c: Bead) -> bool:
        if self.chain_length <= 1:
            return True

        b: Bead = self.beads[-1]
        a: Bead = self.beads[-2]

        ab = Bead((b.x - a.x), (b.y - a.y), (b.z - a.z))
        bc = Bead((c.x - b.x), (c.y - b.y), (c.z - b.z))

        ab_vec = math.sqrt(ab.x ** 2 + ab.y ** 2 + ab.z ** 2)
        bc_vec = math.sqrt(bc.x ** 2 + bc.y ** 2 + bc.z ** 2)

        ab_norm = Bead((ab.x / ab_vec), (ab.y / ab_vec), (ab.z / ab_vec))
        bc_norm = Bead((bc.x / bc_vec), (bc.y / bc_vec), (bc.z / bc_vec))

        res = ab_norm.x * bc_norm.x + ab_norm.y * bc_norm.y + ab_norm.z * bc_norm.z
        angle = math.acos(res) * 180 / math.pi

        if 105 < angle < 120:
            return True
        else:
            return False
        # Получает молекул, которые задевает bead

    def get_neighbor_count(self, bead: Bead) -> int:
        neighbor_count = 0
        for i in self.beads:
            # TODO Проверить формулу
            dist: float = math.sqrt(
                (bead.x - (i.x + bead.x)) ** 2 + (bead.y - (i.y + bead.y)) ** 2 + (bead.z - (i.z + bead.z)) ** 2)

            if dist < C_C_length + DOP_RADIUS:
                neighbor_count += 1

        return neighbor_count


        # Перекрывает ли молекула соседей

    def are_neighbors_exist(self, bead: Bead) -> bool:
        return self.get_neighbor_count(bead) != 0


        # Проверяет не зашли ли за границу коробки

    def check_border(self, bead: Bead) -> bool:
        x = abs(abs(self.beads[-1].x) - abs(bead.x)) < polymer_input.box_x / 2
        y = abs(abs(self.beads[-1].y) - abs(bead.y)) < polymer_input.box_y / 2
        z = abs(abs(self.beads[-1].z) - abs(bead.z)) < polymer_input.box_z / 2

        if x and y and z:
            return True
        else:
            return False

            # Записывает цепочку в файл *.pdb (пока что неправильно)

    def write_to_file(self):
        f = open(os.getcwd() + str(polymer_input.bead_number) + '_' + str(polymer_input.chain_number) + '.pdb', 'a')

        f.write('\n' + str(self.chain_length + len(self.hydrogen)) + ' atoms' + '\n')
        f.write('2 atom types' + '\n' + '\n')
        f.write(str(-polymer_input.box_x / 2 - 1) + ' ' + str(polymer_input.box_x / 2 + 1) + ' xlo xhi' + '\n')
        f.write(str(-polymer_input.box_y / 2 - 1) + ' ' + str(polymer_input.box_y / 2 + 1) + ' ylo yhi' + '\n')
        f.write(str(-polymer_input.box_z / 2 - 1) + ' ' + str(polymer_input.box_z / 2 + 1) + ' zlo zhi' + '\n' + '\n')
        f.write('Masses' + '\n' + '\n' + '1 12.0' + '\n' + '2 1.0' + '\n' + '\n' 'Atoms' + '\n' + '\n')

        for i in range(self.chain_length):
            f.write(str(i + 1) + ' ' + '1 ' + str(self.beads[i].x) + ' ' + str(self.beads[i].y) + ' ' + str(
                self.beads[i].z) + '\n')
        for i in range(len(self.hydrogen)):
            f.write(str(i + 1 + self.chain_length) + ' ' + '2 ' + str(self.hydrogen[i].x) + ' ' + str(
                self.hydrogen[i].y) + ' ' + str(self.hydrogen[i].z) + '\n')

        f.close()


        # TODO переписать

    @staticmethod

    def plot_chain_with_args(args):
        (bead_number, C_in_tubes, C_coord_x, C_coord_y, C_coord_z) = args
        color = ['red', 'green', 'blue', 'yellow', 'black', 'pink']
        fig = pylab.figure()
        ax = Axes3D(fig)

        for i in range(C_in_tubes):
            ax.scatter(C_coord_x[i], C_coord_y[i], C_coord_z[i], c='black')

        for i2 in range(len(C_coord_x) - C_in_tubes):
            i = i2 + C_in_tubes
            ax.scatter(C_coord_x[i], C_coord_y[i], C_coord_z[i], c=color[(i2 // (bead_number + 1)) % len(color)],
                       s=polymer_input.r)

        fig.savefig('chain.png', bbox_inches='tight')

        # TODO ???

    def add_hydrogen(self):
        pass
        # for j in range(len(self.beads)):
        #     i = j + C_IN_TUBES
        #     if j % (polymer_input.bead_number + 2) != 0 and j % (polymer_input.bead_number + 2) != \
        #             (polymer_input.bead_number + 2 - 1):
        #         a_x = (self.beads[i + 1].x - self.beads[i].x) / C_C_length
        #         a_y = (self.beads[i + 1].y - self.beads[i].y) / C_C_length
        #         a_z = (self.beads[i + 1].z - self.beads[i].z) / C_C_length
        #
        #         b_x = (self.beads[i - 1].x - self.beads[i].x) / C_C_length
        #         b_y = (self.beads[i - 1].y - self.beads[i].y) / C_C_length
        #         b_z = (self.beads[i - 1].z - self.beads[i].z) / C_C_length
        #
        #         sin_angle = math.sqrt(1 - (a_x * b_x + a_y * b_y + a_z * b_z) ** 2)
        #
        #         c_x = (a_y * b_z - a_z * b_y) / sin_angle
        #         c_y = (a_z * b_x - a_x * b_z) / sin_angle
        #         c_z = (a_x * b_y - a_y * b_x) / sin_angle
        #
        #         self.hydrogen.append(Bead(
        #             self.beads[i].x + c_x * C_H_LENGTH,
        #             self.beads[i].y + c_y * C_H_LENGTH,
        #             self.beads[i].z + c_z * C_H_LENGTH
        #         ))
        #
        #         self.hydrogen.append(Bead(
        #             self.beads[i].x - c_x * C_H_LENGTH,
        #             self.beads[i].y - c_y * C_H_LENGTH,
        #             self.beads[i].z - c_z * C_H_LENGTH
        #         ))
