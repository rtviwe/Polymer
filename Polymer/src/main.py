import random
import time

from Polymer.src.bead import Bead
from Polymer.src.chain import Chain
from Polymer.src.input import polymer_input

import pylab
from mpl_toolkits.mplot3d import Axes3D

TIME_TO_WAIT = 60  # Сколько времени можно дать, для поиска места новой молекулы в цепочке в секундах


def main():
    chains = []
    flag = False

    for j in range(polymer_input.chain_number):
        while True:
            if flag:
                flag = False
                break
            current_chain = Chain([
                Bead(
                    random.randint(-polymer_input.box_x / 2, polymer_input.box_x / 2),
                    random.randint(-polymer_input.box_y / 2, polymer_input.box_y / 2),
                    random.randint(-polymer_input.box_z / 2, polymer_input.box_z / 2)
                )
            ])
            chains.append(current_chain)

            for i in range(polymer_input.bead_number - 1):
                if flag:
                    break
                start = time.time()
                print('молекула №', current_chain.chain_length, 'в цепочке №', j)

                while True:
                    bead = current_chain.generate()

                    if time.time() - start > TIME_TO_WAIT:
                        flag = True
                        break

                    angle = current_chain.check_angle(bead)
                    neighbor = not current_chain.are_neighbors_exist(bead, chains)
                    border = current_chain.check_border(bead)

                    if angle and neighbor and border:
                        current_chain.add_bead(bead)
                        break

            if len(current_chain.beads) >= polymer_input.bead_number:
                break

    # TODO переписать plot_chain_with_args
    xs = []
    ys = []
    zs = []

    for index, chain in enumerate(chains):
        chain.write_to_file(index)

        for i in chain.beads:
            xs.append(i.x)
            ys.append(i.y)
            zs.append(i.z)

    # Chain.plot_chain_with_args((polymer_input.bead_number, 0, xs, ys, zs))
    plot_chain_with_args(chains)


def plot_chain_with_args(chains: [Chain]):
    color = ['red', 'green', 'blue', 'yellow', 'black', 'pink']
    fig = pylab.figure()
    ax = Axes3D(fig)

    color_index = -1

    for i in chains:
        color_index += 1
        for j in i.beads:
            ax.scatter(j.x, j.y, j.z, c=color[i.id % len(color)], s=polymer_input.r)

    # for i in range(C_in_tubes):
    #     ax.scatter(C_coord_x[i], C_coord_y[i], C_coord_z[i], c='black')
    #
    # for i2 in range(len(C_coord_x) - C_in_tubes):
    #     i = i2 + C_in_tubes
    #     ax.scatter(C_coord_x[i], C_coord_y[i], C_coord_z[i], c=color[(i2 // (bead_number + 1)) % len(color)],
    #                s=polymer_input.r)

    fig.savefig('chain.png', bbox_inches='tight')


# Вот тут надо запускать
if __name__ == "__main__":
    main()
