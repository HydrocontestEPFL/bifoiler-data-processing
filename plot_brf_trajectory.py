import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pandas
import numpy as np
import argparse
import os

from quaternion import *
from velocity_irf2brf import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory containing CSV logs')
    args = parser.parse_args()

    velocity_log = os.path.join(args.dir, '_xsens_publisher_node_filter_xs_velocity.csv')
    position_log = os.path.join(args.dir, '_xsens_publisher_node_filter_xs_latlongalt.csv')
    quaternion_log = os.path.join(args.dir, '_xsens_publisher_node_filter_xs_quaternion.csv')

    vel = pandas.read_csv(velocity_log, sep=';')
    gnss = pandas.read_csv(position_log, sep=';')
    quat = pandas.read_csv(quaternion_log, sep=';')

    subsample = 100

    # position
    r_earth = 6371e3 # m
    lat = gnss['latitude'].values[::subsample]*np.pi/180
    lon = gnss['longitude'].values[::subsample]*np.pi/180
    alt = gnss['altitude'].values[::subsample]

    # ENU
    r = np.stack((
        r_earth*np.sin(lon)*np.cos(np.mean(lat)),
        r_earth*np.sin(lat),
        alt
    ), axis=-1)

    r -= r[0]

    # velocity ENU
    v = vel[['x','y','z']].values[::subsample]
    v_ENU = np.array(v)
    v_scale = 20*np.max(v)

    # quaternion orientation ENU
    quat = quat[['w','x','y','z']].values[::subsample]
    q_ENU = [Quaternion(q) for q in quat]
    q_NED = [q_ENU2NED(q) for q in q_ENU]

    v_brf = vel_irf2brf(v_ENU, q_ENU)

    # Boat reference frame unit vectors NED
    e1_brf = [1,0,0]
    e2_brf = [0,1,0]
    e3_brf = [0,0,1]
    e1_irf = np.array([NED2ENU(qrotate(q, e1_brf)) for q in q_NED])
    e2_irf = np.array([NED2ENU(qrotate(q, e2_brf)) for q in q_NED])
    e3_irf = np.array([NED2ENU(qrotate(q, e3_brf)) for q in q_NED])
    scale = 25

    # project BRF vector to IRF
    v_ENU = v_brf[:,0].reshape(-1,1)*e1_irf + v_brf[:,1].reshape(-1,1)*e2_irf + v_brf[:,2].reshape(-1,1)*e3_irf

    # plot
    fig, ax = plt.subplots()
    ax.quiver(r[:,0], r[:,1], v_ENU[:,0], v_ENU[:,1], color='k', width=0.003, scale=v_scale)
    ax.quiver(r[:,0], r[:,1], e1_irf[:,0], e1_irf[:,1], color='r', width=0.003, scale=scale)
    ax.quiver(r[:,0], r[:,1], e2_irf[:,0], e2_irf[:,1], color='g', width=0.003, scale=scale)
    ax.quiver(r[:,0], r[:,1], e3_irf[:,0], e3_irf[:,1], color='b', width=0.003, scale=scale)
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlabel('East')
    ax.set_ylabel('North')

    fig, ax = plt.subplots(2,1)
    ax[0].quiver(r[:,0], r[:,1], v_ENU[:,0], v_ENU[:,1], color='k', width=0.003, scale=v_scale)
    ax[0].quiver(r[:,0], r[:,1], e1_irf[:,0], e1_irf[:,1], color='r', width=0.003, scale=scale)
    ax[0].quiver(r[:,0], r[:,1], e2_irf[:,0], e2_irf[:,1], color='g', width=0.003, scale=scale)
    ax[0].quiver(r[:,0], r[:,1], e3_irf[:,0], e3_irf[:,1], color='b', width=0.003, scale=scale)
    ax[0].set_aspect('equal', adjustable='datalim')
    ax[0].set_xlabel('East')
    ax[0].set_ylabel('North')

    ax[1].quiver(r[:,0], r[:,2], v_ENU[:,0], v_ENU[:,2], color='k', width=0.003, scale=v_scale)
    ax[1].quiver(r[:,0], r[:,2], e1_irf[:,0], e1_irf[:,2], color='r', width=0.003, scale=scale)
    ax[1].quiver(r[:,0], r[:,2], e2_irf[:,0], e2_irf[:,2], color='g', width=0.003, scale=scale)
    ax[1].quiver(r[:,0], r[:,2], e3_irf[:,0], e3_irf[:,2], color='b', width=0.003, scale=scale)
    ax[1].set_aspect('equal', adjustable='datalim')
    ax[1].set_xlabel('East')
    ax[1].set_ylabel('Up')

    plt.show()


    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.quiver(r[:,0], r[:,1], z, v[:,0], v[:,1], vz, length=1, normalize=True)

if __name__ == '__main__':
    main()
