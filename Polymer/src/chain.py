import os
import random

import math
import pylab
from mpl_toolkits.mplot3d import Axes3D

from src.bead import Bead
from src.input import polymer_input

BEAD_DISTANCE = 1.557  # длина связи между молекулами
ADDITIONAL_RADIUS = 1  # дополнительный радиус, чтобы не ставить молекулы впритык к другим
WALL_PADDING = 10  # расстояние между цепочкой и коробкой
current_chain_id = 0  # переменная, чтобы делать айдишники от 0 до N для цепей


class Chain:
    color = ['red', 'green', 'blue', 'yellow', 'black', 'pink']  # набор всех цветов для рисования в png

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
    def generate(self) -> Bead:
        max_len_x = round(BEAD_DISTANCE + 2 * polymer_input.r)
        x: float = random.randint(self.beads[-1].x - max_len_x,
                                  self.beads[-1].x + max_len_x)

        max_len_y = round(math.sqrt(round(BEAD_DISTANCE + 2 * polymer_input.r) ** 2 - (x - self.beads[-1].x) ** 2))
        y: float = random.randint(self.beads[-1].y - max_len_y,
                                  self.beads[-1].y + max_len_y)

        mediate_value = round(BEAD_DISTANCE + 2 * polymer_input.r) ** 2 - (x - self.beads[-1].x) ** 2 - (
                y - self.beads[-1].y) ** 2
        if mediate_value < 0:
            mediate_value += 1

        z: float = round(math.sqrt(round(mediate_value)) + self.beads[-1].z)

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
    def get_neighbor_count(self, bead: Bead, chains: []) -> int:
        neighbor_count = 0
        for j in chains:
            for i in j.beads:
                dist: float = math.sqrt(
                    (bead.x - (i.x + bead.x)) ** 2 + (bead.y - (i.y + bead.y)) ** 2 + (bead.z - (i.z + bead.z)) ** 2)

                if dist < BEAD_DISTANCE + ADDITIONAL_RADIUS:
                    neighbor_count += 1

        return neighbor_count

    # Перекрывает ли молекула соседей
    def are_neighbors_exist(self, bead: Bead, chains: []) -> bool:
        return self.get_neighbor_count(bead, chains) != 0

    # Проверяет, не зашли ли за границу коробки
    def check_border(self, bead: Bead) -> bool:
        x = abs(abs(self.beads[-1].x) - abs(bead.x)) < polymer_input.box_x / 2
        y = abs(abs(self.beads[-1].y) - abs(bead.y)) < polymer_input.box_y / 2
        z = abs(abs(self.beads[-1].z) - abs(bead.z)) < polymer_input.box_z / 2

        if x and y and z:
            return True
        else:
            return False

    # Записывает цепочку в файл *.pdb в соответсвии с генерацией Avogadro
    def write_to_file(self, index: int):
        f = open(os.getcwd() + str(polymer_input.bead_number) + '_' + str(polymer_input.chain_number) + '.pdb',
                 'a')

        # 1-вид атома 2-номер 3,11-название 4-? 5-количество связей? 6-x координата 7-y координата 8-z координата 9,10-?
        for i in range(self.chain_length):
            X = "{0:.3f}".format(200 + self.beads[i].x)
            Y = "{0:.3f}".format(200 + self.beads[i].y)
            Z = "{0:.3f}".format(200 + self.beads[i].z)
            X = ' ' * (7 - X.find(".")) + X
            Y = ' ' * (3 - Y.find(".")) + Y
            Z = ' ' * (3 - Z.find(".")) + Z
            if i + index * polymer_input.bead_number < 9:
                f.write('HETATM    ' + str(i + 1 + index * polymer_input.bead_number) + '  C   UNL     1 '
                        + X + ' ' + Y + ' ' + Z + '  1.00  0.00           C' + '\n')

            elif i + index * polymer_input.bead_number < 99:
                f.write('HETATM   ' + str(i + 1 + index * polymer_input.bead_number) + '  C   UNL     1 '
                        + X + ' ' + Y + ' ' + Z + '  1.00  0.00           C' + '\n')

            elif i + index * polymer_input.bead_number < 999:
                f.write('HETATM  ' + str(i + 1 + index * polymer_input.bead_number) + '  C   UNL     1 '
                        + X + ' ' + Y + ' ' + Z + '  1.00  0.00           C' + '\n')

            else:
                f.write('HETATM ' + str(i + 1 + index * polymer_input.bead_number) + '  C   UNL     1 '
                        + X + ' ' + Y + ' ' + Z + '  1.00  0.00           C' + '\n')

        for i in range(len(self.hydrogen)):
            f.write(str(i + 1 + self.chain_length) + ' ' + '2 ' + str(self.hydrogen[i].x) + ' ' + str(
                self.hydrogen[i].y) + ' ' + str(self.hydrogen[i].z) + '\n')

        # связи атомов по номерам
        if index + 1 == polymer_input.chain_number:
            for j in range(index + 1):
                f.write('CONECT\t' + str(j * polymer_input.bead_number + 1) + '\t' + str(
                    j * polymer_input.bead_number + 2) + '\n')

                for i in range(polymer_input.bead_number - 2):
                    f.write('CONECT\t' + str(j * polymer_input.bead_number + 2 + i) + '\t' + str(
                        j * polymer_input.bead_number
                        + 3 + i) + '\t' + str(j * polymer_input.bead_number + 1 + i) + '\n')

                f.write('CONECT\t' + str(j * polymer_input.bead_number + polymer_input.bead_number) + '\t'
                        + str(j * polymer_input.bead_number + polymer_input.bead_number - 1) + '\n')

            f.write('END')

        f.close()

    @staticmethod
    def plot_chains(chains):
        color = ['red', 'green', 'blue', 'yellow', 'black', 'pink']
        fig = pylab.figure()
        ax = Axes3D(fig)

        color_index = -1

        for i in chains:
            color_index += 1
            for j in i.beads:
                ax.scatter(j.x, j.y, j.z, c=color[i.id % len(color)], s=polymer_input.r)

        fig.savefig('chain.png', bbox_inches='tight')
