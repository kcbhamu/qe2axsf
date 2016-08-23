#!/usr/bin/python
# input 1 = qe output filename
# input 2 = lattice constant in bohr

import sys

inputname = sys.argv[1]
input = open(inputname, 'r')
outputname = inputname[:-3]+'axsf'
output = open(outputname, 'w')

# find lattice parameter
for line in input:
    if 'lattice parameter' in line:
        list = line.split()
        alat = float(list[4])
        break

# find number of atoms
for line in input:
    if 'number of atoms' in line:
        list = line.split()
        nat = int(list[4])
        break
input.seek(0)

# find number of steps
nsteps = 0
for line in input:
    if 'ATOMIC_POSITIONS' in line:
        nsteps += 1
input.seek(0)

# make axsf file headers
alat_ang = alat/1.889725989
output.write('ANIMSTEPS '+str(nsteps)+'\n')
output.write('CRYSTAL\n')
output.write('PRIMVEC\n')
output.write(str(alat_ang)+' 0 0\n')
output.write('0 '+str(alat_ang)+' 0\n')
output.write('0 0 '+str(alat_ang)+'\n')

# make axsf file body
for i in range(nsteps):
    output.write('PRIMCOORD '+str(i+1)+'\n')
    output.write(str(nat)+' 1\n')
    for line in input:
        if 'ATOMIC_POSITIONS' in line:
            break
    for j in range(3):
        for line in input:
            list = line.split()
            if list[0] == 'O':
                output.write('8 '+list[1]+' '+list[2]+' '+list[3]+'\n')
            elif list[0] == 'H':
                output.write('1 '+list[1]+' '+list[2]+' '+list[3]+'\n')
            else:
                print('error: element not implemented')
            break
