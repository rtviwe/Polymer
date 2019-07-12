import random
import time

from src.bead import Bead
from src.chain import Chain
from src.input import polymer_input

TIME_TO_WAIT = 60  # Сколько времени можно дать, для поиска места новой молекулы в цепочке в секундах


def main():
    chains = []

    for j in range(polymer_input.chain_number):
        while True:
            current_chain = Chain([
                Bead(
                    random.randint(-polymer_input.box_x / 2, polymer_input.box_x / 2),
                    random.randint(-polymer_input.box_y / 2, polymer_input.box_y / 2),
                    random.randint(-polymer_input.box_z / 2, polymer_input.box_z / 2)
                )
            ])
            chains.append(current_chain)

            for i in range(polymer_input.bead_number - 1):
                start = time.time()
                print('молекула №', current_chain.chain_length, 'в цепочке №', j)

                while True:
                    bead = current_chain.generate()

                    if time.time() - start > TIME_TO_WAIT:
                        break

                    angle = current_chain.check_angle(bead)
                    neighbor = not current_chain.are_neighbors_exist(bead)
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

    for chain in chains:
        chain.write_to_file()

        for i in chain.beads:
            xs.append(i.x)

        for i in chain.beads:
            ys.append(i.y)

        for i in chain.beads:
            zs.append(i.z)

    Chain.plot_chain_with_args((polymer_input.bead_number, 0, xs, ys, zs))


# Вот тут надо запускать
if __name__ == "__main__":
    main()
