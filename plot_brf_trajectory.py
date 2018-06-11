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

    # velocity NED
    v = vel[['x','y','z']].values[::subsample]
    # v_ENU = np.array(v)
    v_ENU = np.array([NED2ENU(vv) for vv in v])
    v_scale = 15*np.max(v)

    # quaternion orientation NED
    quat = quat[['w','x','y','z']].values[::subsample]
    # q_ENU = [Quaternion(q) for q in quat]
    q_ENU = [q_NED2ENU(q) for q in quat]

    # Boat reference frame unit vectors
    # e1_I = [1,0,0]
    # e2_I = [0,1,0]
    # e3_I = [0,0,1]
    e1_I = NED2ENU([1,0,0])
    e2_I = NED2ENU([0,1,0])
    e3_I = NED2ENU([0,0,1])
    e1_B = np.array([qrotate(q, e1_I) for q in q_ENU])
    e2_B = np.array([qrotate(q, e2_I) for q in q_ENU])
    e3_B = np.array([qrotate(q, e3_I) for q in q_ENU])
    scale = 20

    # plot
    fig, ax = plt.subplots()
    ax.quiver(r[:,0], r[:,1], v_ENU[:,0], v_ENU[:,1], color='k', width=0.005, scale=v_scale)
    ax.quiver(r[:,0], r[:,1], e1_B[:,0], e1_B[:,1], color='r', width=0.005, scale=scale)
    ax.quiver(r[:,0], r[:,1], e2_B[:,0], e2_B[:,1], color='g', width=0.005, scale=scale)
    ax.quiver(r[:,0], r[:,1], e3_B[:,0], e3_B[:,1], color='b', width=0.005, scale=scale)
    ax.set_aspect('equal', adjustable='datalim')

    fig, ax = plt.subplots(2,2)
    ax[0,1].quiver(r[:,0], r[:,1], v_ENU[:,0], v_ENU[:,1], color='k', width=0.005, scale=v_scale)
    ax[0,1].quiver(r[:,0], r[:,1], e1_B[:,0], e1_B[:,1], color='r', width=0.005, scale=scale)
    ax[0,1].quiver(r[:,0], r[:,1], e2_B[:,0], e2_B[:,1], color='g', width=0.005, scale=scale)
    ax[0,1].quiver(r[:,0], r[:,1], e3_B[:,0], e3_B[:,1], color='b', width=0.005, scale=scale)
    ax[0,1].set_aspect('equal', adjustable='datalim')

    ax[0,0].quiver(r[:,2], r[:,1], v_ENU[:,2], v_ENU[:,1], color='k', width=0.005, scale=v_scale)
    ax[0,0].quiver(r[:,2], r[:,1], e1_B[:,2], e1_B[:,1], color='r', width=0.005, scale=scale)
    ax[0,0].quiver(r[:,2], r[:,1], e2_B[:,2], e2_B[:,1], color='g', width=0.005, scale=scale)
    ax[0,0].quiver(r[:,2], r[:,1], e3_B[:,2], e3_B[:,1], color='b', width=0.005, scale=scale)
    ax[0,0].set_aspect('equal', adjustable='datalim')

    ax[1,1].quiver(r[:,0], r[:,2], v_ENU[:,0], v_ENU[:,2], color='k', width=0.005, scale=v_scale)
    ax[1,1].quiver(r[:,0], r[:,2], e1_B[:,0], e1_B[:,2], color='r', width=0.005, scale=scale)
    ax[1,1].quiver(r[:,0], r[:,2], e2_B[:,0], e2_B[:,2], color='g', width=0.005, scale=scale)
    ax[1,1].quiver(r[:,0], r[:,2], e3_B[:,0], e3_B[:,2], color='b', width=0.005, scale=scale)
    ax[1,1].set_aspect('equal', adjustable='datalim')

    plt.show()


    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.quiver(r[:,0], r[:,1], z, v[:,0], v[:,1], vz, length=1, normalize=True)

if __name__ == '__main__':
    main()
