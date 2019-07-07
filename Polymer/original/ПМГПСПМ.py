import random
import math
import os
import time
import inp

#GLOBAL DATA
vect = 1.557                        #C-C bond length
dop_radius = 1
vect_ch = 0.8                       #C-H bond length
box_x = inp.box_x                   #box size
box_y = inp.box_y
box_z = inp.box_z
time_to_wait = 3                    #lag time (seconds)
bead_number = inp.bead_number       #length of polymer (# of monomers)
chain_numb = inp.chain_numb         #number of polymer chains


#TECHNICAL CONTAINERS
C_coord_x = []
C_coord_y = []
C_coord_z = []

H_coord_x = []
H_coord_y = []
H_coord_z = []


#POLYETHILENE GENERATION

class Chain():

    def __init__(self,coord):
        C_coord_x.extend([coord[0],coord[0]+vect/math.sqrt(2)])
        C_coord_y.extend([coord[1],coord[1]+vect/math.sqrt(2)])
        C_coord_z.extend([coord[2],coord[2]])

    def generate(self):

        phi = random.random()
        theta=random.random()

        self.x=vect*math.sin(2*math.pi*theta)*math.sin(2*math.pi*phi)
        self.y=vect*math.sin(2*math.pi*theta)*math.cos(2*math.pi*phi)
        self.z=vect*math.cos(2*math.pi*theta)


    def check_angle(self):
        x_beg=C_coord_x[-1]
        y_beg=C_coord_y[-1]
        z_beg=C_coord_z[-1]

        x_end=C_coord_x[-2]
        y_end=C_coord_y[-2]
        z_end=C_coord_z[-2]

        COS = ((x_beg - x_end)*(self.x) + (y_beg - y_end)*(self.y) + (z_beg - z_end)*(self.z)) / vect**2
        if(COS > 0.25 and COS < 0.55):
            return 0
        else:
            return 1

    def check_empty(self):
        neigh_count = 0
        for i in range(len(C_coord_x) - 1):
            dist = math.sqrt((C_coord_x[i] - (self.x + C_coord_x[-1]))**2 + (C_coord_y[i] - (self.y + C_coord_y[-1]))**2 + (C_coord_z[i] - (self.z + C_coord_z[-1]))**2)
            if(dist < vect + dop_radius):
                neigh_count += 1
        return neigh_count

    def check_border(self):
        if( abs(C_coord_x[-1] + self.x) < box_x/2 and abs(C_coord_y[-1] + self.y) < box_y/2 and abs(C_coord_z[-1] + self.z) < box_z/2):
            return 0
        else:
            return 1

    def add_bead(self):
        C_coord_x.append(C_coord_x[-1] + self.x)
        C_coord_y.append(C_coord_y[-1] + self.y)
        C_coord_z.append(C_coord_z[-1] + self.z)

    def add_hydr(self):
        for i2 in range(len(C_coord_x) - C_in_tubes):
            i=i2 + C_in_tubes
            if(i2 % (bead_number+2) != 0 and i2 % (bead_number+2) != (bead_number + 2 - 1) ):
                a_x = (C_coord_x[i +1] - C_coord_x[i])/vect
                a_y = (C_coord_y[i +1] - C_coord_y[i])/vect
                a_z = (C_coord_z[i +1] - C_coord_z[i])/vect

                b_x = (C_coord_x[i -1] - C_coord_x[i])/vect
                b_y = (C_coord_y[i -1] - C_coord_y[i])/vect
                b_z = (C_coord_z[i -1] - C_coord_z[i])/vect

                SIN = math.sqrt(1 - (a_x*b_x + a_y*b_y + a_z*b_z)**2)

                c_x = (a_y * b_z - a_z * b_y)/SIN
                c_y = (a_z * b_x - a_x * b_z)/SIN
                c_z = (a_x * b_y - a_y * b_x)/SIN


                H_coord_x.append(C_coord_x[i ] + c_x*vect_ch)
                H_coord_y.append(C_coord_y[i ] + c_y*vect_ch)
                H_coord_z.append(C_coord_z[i ] + c_z*vect_ch)

                H_coord_x.append(C_coord_x[i ] - c_x*vect_ch)
                H_coord_y.append(C_coord_y[i ] - c_y*vect_ch)
                H_coord_z.append(C_coord_z[i ] - c_z*vect_ch)


def write_in_file():
    f = open(os.getcwd() + str(bead_number)+'_'+str(chain_numb)+ '.data','w')


    #GENERATE HEAD OF THE FILE
    f.write('\n' + str(len(C_coord_x) + len(H_coord_x)) + ' atoms' +'\n')
    f.write('2 atom types' + '\n' + '\n')
    f.write(str(-box_x/2 - 1) + ' ' + str(box_x/2 + 1)  + ' xlo xhi' + '\n')
    f.write(str(-box_y/2 - 1) + ' ' + str(box_y/2 + 1)  + ' ylo yhi' + '\n')
    f.write(str(-box_z/2 - 1) + ' ' + str(box_z/2 + 1)  + ' zlo zhi' + '\n' + '\n')
    f.write('Masses' + '\n' + '\n' + '1 12.0' +'\n'+ '2 1.0' + '\n' + '\n' 'Atoms' + '\n' + '\n')


    for i in range(len(C_coord_x)):
        f.write(str(i+1) + ' '+ '1 '  + str(C_coord_x[i])+' '+  str(C_coord_y[i]) +' '+ str(C_coord_z[i]) +'\n')
    for i in range(len(H_coord_x)):
        f.write(str(i+1 + len(C_coord_x)) + ' '+ '2 '  + str(H_coord_x[i])+' '+  str(H_coord_y[i]) +' '+ str(H_coord_z[i]) +'\n')




def create_tube(Diam,L,init_pos,anglex,angley):
    N = round(pi / sin(r/Diam))                                                     #number of atoms in one circle
    r2=r/(2*cos(pi/(2*N)))                                                          #auxiliary vector
    a=[[init_pos[0]],[init_pos[1] - Diam/2],[init_pos[2]]]
    for i in range(N-1):                                                            #first loop

                a[0].append(  round(a[0][i] - r*cos(pi*(2*i + 1)/N),2)  )
                a[1].append(  round(a[1][i] + r*sin(pi*(2*i + 1)/N),2)  )
                a[2].append(  round(a[2][i]))


    for k in range(int(L/tube_coeff)):                                                              #other L loops

        if(k%4 == 2):#(round(k%8,0) == 6) or (round(k%8,0) == 2)):
            for i in range(N):
                a[0].append(  round(a[0][N*k + i] + r2*cos(-pi/(2*N) + 2*pi*i/N),2)  )
                a[1].append(  round(a[1][N*k + i] - r2*sin(-pi/(2*N) + 2*pi*i/N),2)  )
                a[2].append(round(a[2][N*k + i] + 0.5*r/sqrt(3), 2))

        elif(k%4 == 0):#((round(k%8,0) == 0) or (round(k%8,0) == 4)):
            for i in range(N):
                a[0].append(  round(a[0][N*k + i] - r2*cos(-pi/(2*N) + 2*pi*i/N),2)  )
                a[1].append(  round(a[1][N*k + i] + r2*sin(-pi/(2*N) + 2*pi*i/N),2)  )
                a[2].append(round(a[2][N*k + i] + 0.5*r/sqrt(3), 2))

        else:#elif((round(k%8,0) == 1) or (round(k%8,0) == 5) or (round(k%8,0) == 3) or (round(k%8,0) == 7)):
            for i in range(N):
                a[0].append(  round(a[0][N*k + i] ,2)  )
                a[1].append(  round(a[1][N*k + i] ,2)  )
                a[2].append(round(a[2][N*k + i] + r/sqrt(3),2))
    a_cp=[[],[],[]]
    a_cp[0]=a[0][:]
    a_cp[1]=a[1][:]
    a_cp[2]=a[2][:]
    for i in range(len(a[0])):
        a[0][i] = a_cp[0][0] + (a_cp[0][i] - a_cp[0][0])*cos(anglex) - (a_cp[2][i] - a_cp[2][0])*sin(anglex)
        a[2][i] = a_cp[2][0] + (a_cp[0][i] - a_cp[0][0])*sin(anglex) + (a_cp[2][i] - a_cp[2][0])*cos(anglex)

    a_cp[0]=a[0][:]
    a_cp[1]=a[1][:]
    a_cp[2]=a[2][:]

    for i in range(len(a[0])):
        a[1][i] = a_cp[1][0] + (a_cp[1][i] - a_cp[1][0])*cos(angley) - (a_cp[2][i] - a_cp[2][0])*sin(angley)
        a[2][i] = a_cp[2][0] + (a_cp[1][i] - a_cp[1][0])*sin(angley) + (a_cp[2][i] - a_cp[2][0])*cos(angley)

    return a


def apply_tube(Diam,L,init_pos,wall_numb,anglex,angley):
    a_out = [[],[],[]]
    for k in range(wall_numb):
        a_temp = create_tube(Diam - k*dist_btw_walls,L,init_pos,anglex,angley)
        for i in range(len(a_out)):
            a_out[i].extend(a_temp[i])
    return a_out


def add_tube(N,L,a,n,anglex,angley):
    tube_coord = tube.apply_tube(N,L,a,n,anglex,angley)
    C_coord_x.extend(tube_coord[0])
    C_coord_y.extend(tube_coord[1])
    C_coord_z.extend(tube_coord[2])




def main():
    C_in_tubes = len(C_coord_x)

    for j in range(chain_numb):
        while(1):
            first_chain = Chain([random.randint(-box_x/2,box_x/2),random.randint(-box_y/2,box_y/2),random.randint(-box_z/2,box_z/2)])
            chain_len = 2
            for i in range(bead_number):
                start = time.time()
                print(i,chain_len,j)
                while(1):
                    first_chain.generate()
                    if(time.time() - start > time_to_wait):
                        break
                    if(first_chain.check_angle() == 0 and first_chain.check_empty() == 0 and first_chain.check_border() == 0):
                        first_chain.add_bead()
                        chain_len+=1
                        break
                if(time.time() - start > time_to_wait):
                    for k in range(chain_len):
                        C_coord_x.pop(-1)
                        C_coord_y.pop(-1)
                        C_coord_z.pop(-1)
                    break
            if(len(C_coord_x ) - C_in_tubes >= bead_number*(j+1)):
                break


    if(chain_numb != 0):
        first_chain.add_hydr()

    write_in_file()

if __name__ == "__main__":
  main()