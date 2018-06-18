import pandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory containing CSV logs')
    args = parser.parse_args()


    velocity_log = pandas.read_csv(os.path.join(args.dir, '_xsens_publisher_node_filter_xs_velocity.csv'), sep=';')
    vel = velocity_log[['x', 'y']].values
    vel_abs = np.linalg.norm(vel, axis=1)

    position_log = pandas.read_csv(os.path.join(args.dir, '_xsens_publisher_node_filter_xs_latlongalt.csv'), sep=';')
    r = 6371e3 # m
    x = position_log[['longitude']].values*np.pi/180
    y = position_log[['latitude']].values*np.pi/180

    x = r*np.sin(x)*np.cos(np.mean(y))
    y = r*np.sin(y)

    x -= x[0]
    y -= y[0]

    subsample = 100
    x = x[0:-1:subsample]
    y = y[0:-1:subsample]
    velocity = vel_abs[0:-1:subsample]

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be (numlines) x (points per line) x 2 (for x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    fig, axs = plt.subplots(1, 1, sharex=True, sharey=True)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(velocity.min(), velocity.max())
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    # Set the values used for colormapping
    lc.set_array(velocity)
    lc.set_linewidth(1)
    line = axs.add_collection(lc)
    axcb = fig.colorbar(line, ax=axs)
    axcb.set_label('velocity [m/s]')

    axs.set_xlim(x.min(), x.max())
    axs.set_ylim(y.min(), y.max())
    plt.title('Trajectory log')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.savefig('trajectory_log.pdf')
    plt.show()

if __name__ == '__main__':
    main()

