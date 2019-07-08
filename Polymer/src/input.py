# Это все наши входные данные
class Input:

    def __init__(self):
        self.name = 'Polymer'

        # Размеры коробки
        self.box_x = 200
        self.box_y = 200
        self.box_z = 200

        # TODO ???
        self.inclusion_type = 'nanotube'
        self.inclusion_size = 100
        self.inclusion_number = 10
        self.inclusion_chain_length = 5000
        self.density = 0.8

        # TODO ???
        self.step_number = 1000000
        self.step = 0.005
        self.temp = 300
        self.pres = 1
        self.cfg_step = 10000

        # TODO ???
        self.def_step_number = 1000000
        self.def_x = 1
        self.def_y = 1
        self.def_z = 1

        self.bead_number = 20000  # максимум молекул в цепочке
        self.chain_number = 2  # количество цепочек

        self.r = 1  # TODO ???
        self.tube_coefficient = 0.75  # TODO ???

    # TODO переместить весь код снизу сюда
    def request_input(self):
        pass


# Импоритуем эту переменную всюду, где нам нужны входные данные
polymer_input = Input()
isDefault = False

# Здесь она генерится либо по умолчанию, либо через консоль
# TODO добавить все поля сверху на ввод
while True:
    key = input('\n>>>')
    if key == 'start generation default' or key == 'd':
        print('default values')
        isDefault = True
        break
    if key == 'start generation':
        print('Enter parameters:')
        break
    else:
        print('Unknown Command')

while not isDefault:
    key = input('\nJob name =')
    try:
        polymer_input.name = key
        print('Job name = %s' % polymer_input.name)
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nCell size (x y z) =')
    try:
        polymer_input.box_x = float(key.split()[0])
        polymer_input.box_y = float(key.split()[1])
        polymer_input.box_z = float(key.split()[2])
        print('%s x %s x %s Angstrom' % (str(polymer_input.box_x), str(polymer_input.box_y), str(polymer_input.box_z)))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nInclusion type =')
    try:
        polymer_input.inclusion_type = key
        print('Inclusion type: %s' % polymer_input.inclusion_type)
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nInclusion size =')
    try:
        polymer_input.inclusion_size = float(key)
        print('Inclusion size: %s' % str(polymer_input.inclusion_size))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nNumber of inclusions =')
    try:
        polymer_input.inclusion_number = int(key)
        print('Number of inclusions: %s' % str(polymer_input.inclusion_number))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nPolymer chain length =')
    try:
        polymer_input.inclusion_chain_length = int(key)
        print('Polymer chain length: %s' % str(polymer_input.inclusion_chain_length))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nDensity =')
    try:
        polymer_input.density = float(key)
        print('Density: %s g/cm3' % str(polymer_input.density))
        break
    except:
        print('wrong data type')

print('\n\nGenerated file "%s.data"' % polymer_input.name)

isDefault = False

while True:
    key = input('\n>>>')
    if key == 'start relaxation default' or key == 'd':
        print('default values')
        isDefault = True
        break
    if key == 'start relaxation':
        print('Enter parameters:')
        break
    else:
        print('Unknown Command')

while not isDefault:
    key = input('\nNumber of steps =')
    try:
        polymer_input.step_numb = int(key)
        print('Number of steps: %s' % str(polymer_input.step_numb))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nStep (ps) =')
    try:
        polymer_input.step = float(key)
        print('Step:%s ps' % str(polymer_input.step))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nTemperature =')
    try:
        polymer_input.temp = float(key)
        print('Temperature: %s' % str(polymer_input.temp))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nPressure (bar) =')
    try:
        polymer_input.pres = float(key)
        print('Pressure: %s bar' % str(polymer_input.pres))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nGenerate cfg every X steps =')
    try:
        polymer_input.cfg_step = int(key)
        print('Generate cfg every %s steps' % str(polymer_input.cfg_step))
        break
    except:
        print('wrong data type')

print('\n\nGenerated in-file "in_relax.%s"' % polymer_input.name)

isDefault = False

while True:
    key = input('\n>>>')
    if key == 'start deformation default' or key == 'd':
        print('default values')
        isDefault = True
        break
    if key == 'start deformation':
        print('Enter parameters:')
        break
    else:
        print('Unknown Command')

while not isDefault:
    key = input('\nNumber of steps (deformation) =')
    try:
        polymer_input.def_step_number = int(key)
        print('Number of steps: %s' % str(polymer_input.def_step_number))
        break
    except:
        print('wrong data type')

while not isDefault:
    key = input('\nDeformation (dx dy dz) =')
    try:
        polymer_input.def_x = float(key.split()[0])
        polymer_input.def_y = float(key.split()[1])
        polymer_input.def_z = float(key.split()[2])
        print(
            'Deformation %s x %s x %s Angstrom' % (
            str(polymer_input.def_x), str(polymer_input.def_y), str(polymer_input.def_z)))
        break
    except:
        print('wrong data type')

print('\n\nGenerated in-file "in_deform.%s"' % polymer_input.name)
