import matplotlib.pyplot as plt
import numpy as np
import pandas
import datetime
import argparse

def make_time(secs, nsecs):
    date = datetime.datetime.fromtimestamp(secs)
    date = date.replace(microsecond=int(nsecs/1000))
    date.isoformat(timespec='microseconds')
    return date

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='CSV velocity log file')
    parser.add_argument('--subsample', default=5, type=int, help='subsample for faster plotting')
    args = parser.parse_args()

    df = pandas.read_csv(args.file, sep=';')
    t = df[['secs', 'nsecs']].copy().values[::args.subsample,:]
    vel = df[['x', 'y', 'z']].copy().values[::args.subsample,:]

    t = [make_time(s, ns) for s, ns in t]

    vel_abs = np.linalg.norm(vel[:,0:2], axis=1)

    plt.title('Velocity')
    plt.xlabel('time [s]')
    plt.ylabel('v [m/s]')
    plt.plot(t, vel_abs)
    plt.gcf().autofmt_xdate()
    plt.show()

if __name__ == '__main__':
    main()
