import pandas
import numpy as np
import argparse
import os

from quaternion import *

def q_ENU2NED(q):
    return Quaternion([q[0]] + ENU2NED(q[1:]))

def ENU2NED(v):
    return [v[1], v[0], -v[2]]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory containing CSV logs')
    parser.add_argument('outfile', help='CSV output file name')
    args = parser.parse_args()

    quaternion_log = os.path.join(args.dir, '_xsens_publisher_node_filter_xs_quaternion.csv')

    quat = pandas.read_csv(quaternion_log, sep=';')

    # quaternion orientation ENU
    q_ENU = [Quaternion(q) for q in quat[['w','x','y','z']].values]
    # q_NED = np.empty(len(q_ENU, 4))
    q_NED = np.array([list(q_ENU2NED(q)) for q in q_ENU])

    df = pandas.DataFrame(q_NED, columns=['x', 'y', 'z', 'w'])
    time = quat[['time_stamp', 'seq', 'secs', 'nsecs']].copy()
    out = pandas.concat([time, df], axis=1)

    # write CSV
    if args.outfile is not None:
        out.to_csv(args.outfile, sep=';')
        # out.to_csv(args.outfile, sep=';', index=False)
        print('wrote {} lines to {}'.format(len(out)+1, args.outfile))

if __name__ == '__main__':
    main()
