import numpy as np


def convert(POSCAR):
    """
    Read the POSCAR file.
    """
    with open(POSCAR, 'r') as f:
        lines = f.readlines()
        scale = float(lines[1])
        lattice = np.array([list(map(float, line.split())) for line in lines[2:5]])
        species = lines[5].split()
        numbers = list(map(int, lines[6].split()))
        positions = np.array([list(map(float, line.split())) for line in lines[8:]])
    # Get the coordinates type
    if 'DIRECT' in lines[7].upper():
        frac2cart(scale, lattice, species, numbers, positions)
    elif 'CARTESIAN' in lines[7].upper():
        cart2frac(scale, lattice, species, numbers, positions)

def cart2frac(scale, lattice, species, numbers, positions):
    """
    Convert cartesian coordinates to fractional coordinates.
    """
    inv_lattice = np.linalg.inv(lattice)
    scaled_lattice = lattice * scale
    frac_positions = np.dot(positions, inv_lattice)
    write_POSCAR(scaled_lattice, species, numbers, frac_positions, True)


def frac2cart(scale, lattice, species, numbers, positions):
    """
    Convert fractional coordinates to cartesian coordinates.
    """
    scaled_lattice = lattice * scale
    cart_positions = np.dot(positions, scaled_lattice)
    write_POSCAR(scaled_lattice, species, numbers, cart_positions, False)

def write_POSCAR(lattice, species, numbers, positions, is_frac):
    """
    Write the POSCAR file.
    """
    # Write POSCAR_converted
    if is_frac:
        POSCAR_Converted = 'POSCAR_Frac.vasp'
    else:
        POSCAR_Converted = 'POSCAR_Cart.vasp'
    with open(POSCAR_Converted, 'w') as f:
        f.write('Converted POSCAR\n')
        f.write('1.0\n')
        for i in range(3):
            f.write('        ' + '    '.join(str(x).ljust(20, '0') for x in lattice[i]) + '\n')
        f.write('    ' + ''.join(str(x).ljust(8) for x in species) + '\n')
        f.write('    ' + ''.join(str(x).ljust(8) for x in numbers) + '\n')
        if is_frac:
            f.write('Direct\n')
        else:
            f.write('Cartesian\n')
        for pos in positions:
            f.write('    ' + '    '.join(str(x).ljust(20, '0') for x in pos) + '\n')

if __name__ == '__main__':
    POSCAR = 'POSCAR.vasp'
    convert(POSCAR)


