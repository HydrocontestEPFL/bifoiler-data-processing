import matplotlib.pyplot as plt
import pandas
import numpy as np
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory containing CSV logs')
    parser.add_argument('outfile', help='CSV output file name', nargs='?')
    parser.add_argument('--plot', help='flag to enable plot', action='store_true')
    args = parser.parse_args()

    position_log = os.path.join(args.dir, '_xsens_publisher_node_filter_xs_latlongalt.csv')

    gnss = pandas.read_csv(position_log, sep=';')

    # position
    r_earth = 6371e3 # m
    lat = gnss['latitude'].values*np.pi/180
    lon = gnss['longitude'].values*np.pi/180
    alt = gnss['altitude'].values

    # NED
    r = np.stack((
        r_earth*np.sin(lat), # north
        r_earth*np.sin(lon)*np.cos(np.mean(lat)), # east
        -alt # down
    ), axis=-1)

    r -= r[0]

    df = pandas.DataFrame(r, columns=['x', 'y', 'z'])
    time = gnss[['time_stamp', 'seq', 'secs', 'nsecs']].copy()
    out = pandas.concat([time, df], axis=1)

    # write CSV
    if args.outfile is not None:
        out.to_csv(args.outfile, sep=';')
        print('wrote {} lines to {}'.format(len(out)+1, args.outfile))

    # plot
    if args.plot:
        out[['x','y']].plot(x='y', y='x')
        plt.show()
        out['z'].plot()
        plt.show()

if __name__ == '__main__':
    main()
