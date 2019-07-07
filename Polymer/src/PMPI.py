import os
import sys

MPNCS_ver = '1.0'
Python_ver = sys.version[:6]
LAMMPS_version = s = os.popen('echo "quit" | ./LAMMPS/lmp_polymer').read().replace("\n", "")
print('Multiscale Polymer NanoComposite Simusator v %s' % MPNCS_ver)
print('Python v %s' % Python_ver)
print('Lammps library package %s' % LAMMPS_version)


class Input:

    def __init__(self):
        self.name = 'default task'
        self.box_x = 200
        self.box_y = 200
        self.box_z = 200
        self.inc_type = 'nanotube'
        self.inc_size = 100
        self.inc_numb = 10
        self.inc_ch_length = 5000
        self.density = 0.8

        self.step_numb = 1000000
        self.step = 0.005
        self.temp = 300
        self.pres = 1
        self.cfg_step = 10000

        self.def_step_numb = 1000000
        self.def_x = 1
        self.def_y = 1
        self.def_z = 1


pmpi_input = Input()
default_flag = 0

while True:
    key = input('\n>>>')
    if key == 'start generation default':
        print('default values')
        default_flag = 1
        break
    if key == 'start generation':
        print('Enter parameters:')
        break
    else:
        print('Unknown Command')

while True * (not default_flag):
    key = input('\nJob name =')
    try:
        Input.name = key
        print('Job name = %s' % Input.name)
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nCell size (x y z) =')
    try:
        Input.box_x = float(key.split()[0])
        Input.box_y = float(key.split()[1])
        Input.box_z = float(key.split()[2])
        print('%s x %s x %s Angstrom' % (str(Input.box_x), str(Input.box_y), str(Input.box_z)))
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nInclusion type =')
    try:
        Input.inc_type = key
        print('Inclusion type: %s' % Input.inc_type)
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nInclusion size =')
    try:
        Input.inc_size = float(key)
        print('Inclusion size: %s' % str(Input.inc_size))
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nNumber of inclusions =')
    try:
        Input.inc_numb = int(key)
        print('Number of inclusions: %s' % str(Input.inc_numb))
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nPolymer chain length =')
    try:
        Input.inc_ch_length = int(key)
        print('Polymer chain length: %s' % str(Input.inc_ch_length))
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nDensity =')
    try:
        Input.density = float(key)
        print('Density: %s g/cm3' % str(Input.density))
        break
    except:
        print('wrong data type')

print('\n\nGenerated file "%s.data"' % Input.name)

default_relax_flag = 0
while True:
    key = input('\n>>>')
    if key == 'start relaxation default':
        print('default values')
        default_relax_flag = 1
        break
    if key == 'start relaxation':
        print('Enter parameters:')
        break
    else:
        print('Unknown Command')

while True * (not default_relax_flag):
    key = input('\nNumber of steps =')
    try:
        Input.step_numb = int(key)
        print('Number of steps: %s' % str(Input.step_numb))
        break
    except:
        print('wrong data type')

while True * (not default_relax_flag):
    key = input('\nStep (ps) =')
    try:
        Input.step = float(key)
        print('Step:%s ps' % str(Input.step))
        break
    except:
        print('wrong data type')

while True * (not default_relax_flag):
    key = input('\nTemperature =')
    try:
        Input.temp = float(key)
        print('Temperature: %s' % str(Input.temp))
        break
    except:
        print('wrong data type')

while True * (not default_relax_flag):
    key = input('\nPressure (bar) =')
    try:
        Input.pres = float(key)
        print('Pressure: %s bar' % str(Input.pres))
        break
    except:
        print('wrong data type')

while True * (not default_relax_flag):
    key = input('\nGenerate cfg every X steps =')
    try:
        Input.cfg_step = int(key)
        print('Generate cfg every %s steps' % str(Input.cfg_step))
        break
    except:
        print('wrong data type')

print('\n\nGenerated in-file "in_relax.%s"' % Input.name)

default_def_flag = 0
while True:
    key = input('\n>>>')
    if key == 'start deformation default':
        print('default values')
        default_def_flag = 1
        break
    if key == 'start deformation':
        print('Enter parameters:')
        break
    else:
        print('Unknown Command')

while True * (not default_def_flag):
    key = input('\nNumber of steps (deformation) =')
    try:
        Input.def_step_numb = int(key)
        print('Number of steps: %s' % str(Input.def_step_numb))
        break
    except:
        print('wrong data type')

while True * (not default_def_flag):
    key = input('\nDeformation (dx dy dz) =')
    try:
        Input.def_x = float(key.split()[0])
        Input.def_y = float(key.split()[1])
        Input.def_z = float(key.split()[2])
        print('Deformation %s x %s x %s Angstrom' % (str(Input.def_x), str(Input.def_y), str(Input.def_z)))
        break
    except:
        print('wrong data type')

print('\n\nGenerated in-file "in_deform.%s"' % Input.name)
