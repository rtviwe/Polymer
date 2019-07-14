# Это все наши входные данные
class Input:

    def __init__(self):
        self.name = 'Polymer'

        # Размеры коробки
        self.box_x = 200
        self.box_y = 200
        self.box_z = 200

        # TODO ???
        self.nanotube_size = 100 # размер нанотрубок, ввод пока что убрал
        self.nanotube_number = 10 # кол-во нанотрубок,ввод пока что убрал

        # TODO ???
        self.bead_number = 2000  # максимум молекул в цепочке
        self.chain_number = 2  # количество цепочек
        self.temp = 300  # температура
        self.r = 3  # радиус молекулы

    # TODO переместить весь код снизу сюда
    def request_input(self):
        pass


# Импоритуем эт у переменную всюду, где нам нужны входные данные
polymer_input = Input()
isDefault = False

# Здесь она генерится либо по умолчанию, либо через консоль
# TODO добавить все поля сверху на ввод
while True:
    key = input('\nGeneral settings>>>')
    if key == 'start generation default' or key == 'd':
        print('default values')
        isDefault = True
        break
    if key == 'start':
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

print('\n\nGenerated file "%s.data"' % polymer_input.name)

isDefault = False

while True:
    key = input('\nPolymer settings>>>')
    if key == 'start relaxation default' or key == 'd':
        print('default values')
        isDefault = True
        break
    if key == 'start':
        print('Enter parameters:')
        break
    else:
        print('Unknown Command')
while not isDefault:
    key = input('\nPolymer chain length =')
    try:
        polymer_input.bead_number = int(key)
        print('Polymer chain length: %s' % str(polymer_input.bead_number))
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
    key = input('\nRadius =')
    try:
        polymer_input.r = float(key)
        print('Radius: %s' % str(polymer_input.r))
        break
    except:
        print('wrong data type')
while not isDefault:
    key = input('\nChain number =')
    try:
        polymer_input.chain_number = int(key)
        print('Chain number: %s' % str(polymer_input.chain_number))
        break
    except:
        print('wrong data type')

print('\n\nGenerated in-file "in_relax.%s"' % polymer_input.name)

