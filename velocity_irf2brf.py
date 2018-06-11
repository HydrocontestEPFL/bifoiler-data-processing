import matplotlib.pyplot as plt
import pandas
import numpy as np
import argparse

from quaternion import *

# in ENU inertial reference frame
v = [4.25936126709, 1.84786343575, -0.189002215862]
q = Quaternion([-0.963283419609, -0.265894293785, 0.0170159712434, -0.033102504909])

def qrotate(q, v):
    qv = Quaternion([0]+v)
    qv = q * qv * q.conjugated()
    # qv = q * qv * q.inverse()
    return list(qv)[1:]

def qrotate_inverse(q, v):
    return qrotate(q.conjugated(), v)
    # return qrotate(q.inverse(), v)

def q_ENU2NED(q):
    return Quaternion([q[0]] + ENU2NED(q[1:]))

def ENU2NED(v):
    return [v[1], v[0], -v[2]]

def velocity_irf2brf(q_BI, v):
    return qrotate_inverse(q_BI, v)


print(v)
print(ENU2NED(v))
print(q)
print(q_ENU2NED(q))

print(velocity_irf2brf(q, v))
print(velocity_irf2brf(q_ENU2NED(q), ENU2NED(v)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('velocity_log', help='Velocity CSV log')
    parser.add_argument('quaternion_log', help='Quaternion orientation CSV log')
    parser.add_argument('outfile', help='CSV output file name')
    args = parser.parse_args()

    src = pandas.read_csv(args.velocity_log, sep=';')

    # out.to_csv(args.outfile, sep=';')
    # print('wrote {} lines to {}'.format(len(out)+1, args.outfile))

if __name__ == '__main__':
    main()
