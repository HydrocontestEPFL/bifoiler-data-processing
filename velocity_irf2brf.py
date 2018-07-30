import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pandas
import numpy as np
import argparse
import os

from quaternion import *

def qrotate(q, v):
    qv = Quaternion([0]+list(v))
    qv = q * qv * q.conjugated()
    return list(qv)[1:]

def qrotate_inverse(q, v):
    return qrotate(q.conjugated(), v)

def q_ENU2NED(q):
    return Quaternion([q[0]] + ENU2NED(q[1:]))

def ENU2NED(v):
    return [v[1], v[0], -v[2]]

def q_NED2ENU(q):
    return q_ENU2NED(q)

def NED2ENU(v):
    return ENU2NED(v)

def vel_irf2brf(v_ENU, q_ENU):
    # v_brf = np.array([ENU2NED(qrotate_inverse(q, v)) for q, v in zip(q_ENU, v_ENU)])

    v_NED = [ENU2NED(vv) for vv in v_ENU]
    q_NED = [q_ENU2NED(q) for q in q_ENU]
    v_brf = np.array([qrotate_inverse(q, v) for q, v in zip(q_NED, v_NED)])

    return v_brf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory containing CSV logs')
    parser.add_argument('outfile', help='CSV output file name', nargs='?')
    parser.add_argument('--plot', help='flag to enable plot', action='store_true')
    args = parser.parse_args()

    velocity_log = os.path.join(args.dir, '_xsens_publisher_node_filter_xs_velocity.csv')
    quaternion_log = os.path.join(args.dir, '_xsens_publisher_node_filter_xs_quaternion.csv')

    vel = pandas.read_csv(velocity_log, sep=';')
    quat = pandas.read_csv(quaternion_log, sep=';')

    # boat reference frame:
    # x forward
    # y left
    # z up

    # velocity data seems to be in NED reference frame (even if data log states otherwise)

    # TODO: verify correct reference frame and orientation.
    # reference frames were deduced purely from datalogs and what seemed to make sense
    # this should be verified by proper tests (and by checking the sensor configuration)

    # velocity ENU
    v_ENU = vel[['x','y','z']].values

    # quaternion orientation ENU
    q_ENU = [Quaternion(q) for q in quat[['w','x','y','z']].values]

    v_brf = vel_irf2brf(v_ENU, q_ENU)

    df = pandas.DataFrame(v_brf, columns=['x', 'y', 'z'])
    time = vel[['time_stamp', 'seq', 'secs', 'nsecs']].copy()
    out = pandas.concat([time, df], axis=1)

    # write CSV
    if args.outfile is not None:
        out.to_csv(args.outfile, sep=';')
        print('wrote {} lines to {}'.format(len(out)+1, args.outfile))

    # plot
    if args.plot:
        out[['x','y','z']].plot()
        plt.show()

if __name__ == '__main__':
    main()
