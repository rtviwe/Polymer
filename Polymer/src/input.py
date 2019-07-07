# Это все наши входные данные
class Input:

    def __init__(self):
        self.name = 'default task'
        self.box_x = 200
        self.box_y = 200
        self.box_z = 200
        self.inclusion_type = 'nanotube'
        self.inclusion_size = 100
        self.inclusion_number = 10
        self.inclusion_chain_length = 5000
        self.density = 0.8

        self.step_number = 1000000
        self.step = 0.005
        self.temp = 300
        self.pres = 1
        self.cfg_step = 10000

        self.def_step_number = 1000000
        self.def_x = 1
        self.def_y = 1
        self.def_z = 1

        # TODO not sure
        self.bead_number = 5
        self.chain_number = 2
        self.chain_length = 2
        self.r = 10
        self.tube_coefficient = 0.75


# Импоритуем эту переменную всюду, где нам нужны входные данные
pmpi_input = Input()
default_flag = 0

# Здесь она генерится либо по умолчанию, либо через консоль
while True:
    key = input('\n>>>')
    if key == 'start generation default' or key == 'd':
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
        pmpi_input.name = key
        print('Job name = %s' % pmpi_input.name)
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nCell size (x y z) =')
    try:
        pmpi_input.box_x = float(key.split()[0])
        pmpi_input.box_y = float(key.split()[1])
        pmpi_input.box_z = float(key.split()[2])
        print('%s x %s x %s Angstrom' % (str(pmpi_input.box_x), str(pmpi_input.box_y), str(pmpi_input.box_z)))
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nInclusion type =')
    try:
        pmpi_input.inclusion_type = key
        print('Inclusion type: %s' % pmpi_input.inclusion_type)
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nInclusion size =')
    try:
        pmpi_input.inclusion_size = float(key)
        print('Inclusion size: %s' % str(pmpi_input.inclusion_size))
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nNumber of inclusions =')
    try:
        pmpi_input.inclusion_number = int(key)
        print('Number of inclusions: %s' % str(pmpi_input.inclusion_number))
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nPolymer chain length =')
    try:
        pmpi_input.inclusion_chain_length = int(key)
        print('Polymer chain length: %s' % str(pmpi_input.inclusion_chain_length))
        break
    except:
        print('wrong data type')

while True * (not default_flag):
    key = input('\nDensity =')
    try:
        pmpi_input.density = float(key)
        print('Density: %s g/cm3' % str(pmpi_input.density))
        break
    except:
        print('wrong data type')

print('\n\nGenerated file "%s.data"' % pmpi_input.name)

default_relax_flag = 0
while True:
    key = input('\n>>>')
    if key == 'start relaxation default' or key == 'd':
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
        pmpi_input.step_numb = int(key)
        print('Number of steps: %s' % str(pmpi_input.step_numb))
        break
    except:
        print('wrong data type')

while True * (not default_relax_flag):
    key = input('\nStep (ps) =')
    try:
        pmpi_input.step = float(key)
        print('Step:%s ps' % str(pmpi_input.step))
        break
    except:
        print('wrong data type')

while True * (not default_relax_flag):
    key = input('\nTemperature =')
    try:
        pmpi_input.temp = float(key)
        print('Temperature: %s' % str(pmpi_input.temp))
        break
    except:
        print('wrong data type')

while True * (not default_relax_flag):
    key = input('\nPressure (bar) =')
    try:
        pmpi_input.pres = float(key)
        print('Pressure: %s bar' % str(pmpi_input.pres))
        break
    except:
        print('wrong data type')

while True * (not default_relax_flag):
    key = input('\nGenerate cfg every X steps =')
    try:
        pmpi_input.cfg_step = int(key)
        print('Generate cfg every %s steps' % str(pmpi_input.cfg_step))
        break
    except:
        print('wrong data type')

print('\n\nGenerated in-file "in_relax.%s"' % pmpi_input.name)

default_def_flag = 0
while True:
    key = input('\n>>>')
    if key == 'start deformation default' or key == 'd':
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
        pmpi_input.def_step_number = int(key)
        print('Number of steps: %s' % str(pmpi_input.def_step_number))
        break
    except:
        print('wrong data type')

while True * (not default_def_flag):
    key = input('\nDeformation (dx dy dz) =')
    try:
        pmpi_input.def_x = float(key.split()[0])
        pmpi_input.def_y = float(key.split()[1])
        pmpi_input.def_z = float(key.split()[2])
        print(
            'Deformation %s x %s x %s Angstrom' % (str(pmpi_input.def_x), str(pmpi_input.def_y), str(pmpi_input.def_z)))
        break
    except:
        print('wrong data type')

print('\n\nGenerated in-file "in_deform.%s"' % pmpi_input.name)
