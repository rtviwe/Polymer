import random
import time

from Polymer.src.bead import Bead
from Polymer.src.chain import Chain
from Polymer.src.input import polymer_input

TIME_TO_WAIT = 1  # Сколько времени можно дать, для поиска места новой молекулы в цепочке в секундах


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

    for index, chain in enumerate(chains):
        chain.write_to_file(index)

    Chain.plot_chains(chains)


if __name__ == "__main__":
    main()
