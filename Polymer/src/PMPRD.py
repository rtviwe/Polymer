import os

import pylab
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

from Polymer.src.PMGPSPM import h_coord_x, h_coord_y, h_coord_z
from Polymer.src.PMPI import pmpi_input
from Polymer.src.PVBzPB import Lammps

lmp = Lammps()


def gen_in_file(args):
    text = '''
units           metal
atom_style      atomic
boundary        p p p

pair_style     airebo   1.5

read_data       %s

pair_coeff * *  CH.airebo C H

timestep        %s

thermo  100
thermo_style    custom step temp  etotal vol press pe epair xlo xhi pxx pyy pzz

fix             3 all nvt temp %s %s 0.01
run             %s

fix             2 all deform 1 x final 0 %s y final 0 %s z final 0 %s units box
dump            2 all cfg %s  %s.*.cfg id type xs ys zs
dump_modify     2 element C H
run             %s

unfix	1
fix             2 all nvt temp %s  %s 0.01
dump_modify     2 element C H
run             %s
''' % args
    in_file = open(os.getcwd() + '/in.deform')
    in_file.writelines(text)


def plot_chain_with_args(args):
    (bead_number, C_in_tubes, C_coord_x, C_coord_y, C_coord_z) = args
    color = ['red', 'green', 'blue', 'yellow', 'black', 'pink']
    fig = pylab.figure()
    ax = Axes3D(fig)
    for i in range(C_in_tubes):
        ax.scatter(C_coord_x[i], C_coord_y[i], C_coord_z[i], c='black')
    for i2 in range(len(C_coord_x) - C_in_tubes):
        i = i2 + C_in_tubes
        ax.scatter(C_coord_x[i], C_coord_y[i], C_coord_z[i], c=color[(i2 // (bead_number + 2)) % len(color)])
    pyplot.show()


def write_in_file_with_args(args):
    (chain_numb, bead_number, C_in_tubes, C_coord_x, C_coord_y, C_coord_z) = args

    f = open(os.getcwd() + str(bead_number) + '_' + str(chain_numb) + '.data', 'w')

    # Generate head of file
    f.write('\n' + str(len(C_coord_x) + len(h_coord_x)) + ' atoms' + '\n')
    f.write('2 atom types' + '\n' + '\n')
    f.write(str(-pmpi_input.box_x / 2 - 1) + ' ' + str(pmpi_input.box_x / 2 + 1) + ' xlo xhi' + '\n')
    f.write(str(-pmpi_input.box_y / 2 - 1) + ' ' + str(pmpi_input.box_y / 2 + 1) + ' ylo yhi' + '\n')
    f.write(str(-pmpi_input.box_z / 2 - 1) + ' ' + str(pmpi_input.box_z / 2 + 1) + ' zlo zhi' + '\n' + '\n')
    f.write('Masses' + '\n' + '\n' + '1 12.0' + '\n' + '2 1.0' + '\n' + '\n' 'Atoms' + '\n' + '\n')

    for i in range(len(C_coord_x)):
        f.write(str(i + 1) + ' ' + '1 ' + str(C_coord_x[i]) + ' ' + str(C_coord_y[i]) + ' ' + str(C_coord_z[i]) + '\n')
    for i in range(len(h_coord_x)):
        f.write(str(i + 1 + len(C_coord_x)) + ' ' + '2 ' + str(h_coord_x[i]) + ' ' + str(h_coord_y[i]) + ' ' + str(
            h_coord_z[i]) + '\n')
