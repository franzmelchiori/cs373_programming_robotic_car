#!/usr/bin/python


################################################################################
#                                                                              #
"""  CS373: Programming a Robotic Car
     Homework of Unit 01
     Localizer
"""
#   Francesco Melchiori, 2011, 2012                                            #
#   melchiori@disi.unitn.it                                                    #
#   NiLab FBK CIMeC DISI UniTN                                                 #
#                                                                              #
################################################################################


colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]


# colors = [['green', 'green', 'green'],
#           ['green', 'red',   'red'],
#           ['green', 'green', 'green']]

# measurements = ['red', 'red']
# motions = [[0, 0], [0, 1]]


sensor_right = 0.7
p_move = 0.8


def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

def initialization():
    p = []
    for rw in range(len(colors)):
        p.append([])
        for cl in range(len(colors[0])):
            p[rw].append(.0)
    return p

def uniform(p):
    s = len(p) * len(p[0])
    for rw in range(len(p)):
        for cl in range(len(p[0])):
            p[rw][cl] = 1./s
    return p

def sense(p, Z):
    q = initialization()
    for rw in range(len(q)):
        for cl in range(len(q[0])):
            if Z == colors[rw][cl]:
                q[rw][cl] = p[rw][cl] * sensor_right
            else:
                q[rw][cl] = p[rw][cl] * (1-sensor_right)
    s = sum(sum(q[i]) for i in range(len(q)))
    for rw in range(len(q)):
        for cl in range(len(q[0])):
            q[rw][cl] /= s
    return q

def move(p, M):
    q = initialization()
    for rw in range(len(q)):
        for cl in range(len(q[0])):
            if M == [ 0,  0]: # no move
                q[rw][cl] = q[rw][cl] + (p[rw][cl] * p_move) +\
                                        (p[rw][cl] * (1 - p_move))
            if M == [ 0,  1]: # right
                q[rw][cl] = q[rw][cl] + (p[rw][cl-1] * p_move) +\
                                        (p[rw][cl] * (1 - p_move))
            if M == [ 0, -1]: # left
                if cl+1 != len(q[0]):
                    q[rw][cl] = q[rw][cl] + (p[rw][cl+1] * p_move) +\
                                            (p[rw][cl] * (1 - p_move))
                else:
                    q[rw][cl] = q[rw][cl] + (p[rw][0] * p_move) +\
                                            (p[rw][cl] * (1 - p_move))
            if M == [ 1,  0]: # down
                if rw != 0:
                    q[rw][cl] = q[rw][cl] + (p[rw-1][cl] * p_move) +\
                                            (p[rw][cl] * (1 - p_move))
                else:
                    q[rw][cl] = q[rw][cl] + (p[-1][cl] * p_move) +\
                                            (p[rw][cl] * (1 - p_move))
            if M == [-1,  0]: # up
                if rw+1 != len(q):
                    q[rw][cl] = q[rw][cl] + (p[rw+1][cl] * p_move) +\
                                            (p[rw][cl] * (1 - p_move))
                else:
                    q[rw][cl] = q[rw][cl] + (p[0][cl] * p_move) +\
                                            (p[rw][cl] * (1 - p_move))
    return q

p = initialization()
p = uniform(p)
for k in range(len(measurements)):
    M = motions[k]
    p = move(p, M)
    Z = measurements[k]
    p = sense(p, Z)

show(p)
