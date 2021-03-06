import matplotlib.pyplot as plt
import pandas
import numpy as np
import argparse

# settings (measured)
RIGHT_FLAP_CHANNEL = 5
RIGHT_FLAP_GAIN = 0.0008667
RIGHT_FLAP_OFFSET = -1500 * RIGHT_FLAP_GAIN

LEFT_FLAP_CHANNEL = 4
LEFT_FLAP_GAIN = -0.0009786
LEFT_FLAP_OFFSET = -1500 * LEFT_FLAP_GAIN

RUDDER_CHANNEL = 2
RUDDER_GAIN = 0.001347
RUDDER_OFFSET = -2.029

THRUST_CHANNEL = 1
THRUST_GAIN = 1.0/500 # thrust PWM between 1500us and 2000us
THRUST_OFFSET = -1500 * THRUST_GAIN

def channel_line(ch):
    return [int(i) for i in ch.strip('[] ').split(',')]

def parse_channels(ch):
    df = pandas.DataFrame()
    ch = np.array([channel_line(line) for line in ch])
    left = ch[:,LEFT_FLAP_CHANNEL-1] * LEFT_FLAP_GAIN + LEFT_FLAP_OFFSET
    right = ch[:,RIGHT_FLAP_CHANNEL-1] * RIGHT_FLAP_GAIN + RIGHT_FLAP_OFFSET
    df['flaps'] = (left - right) / 2
    df['aileron'] = (left + right) / 2
    df['rudder'] = ch[:,RUDDER_CHANNEL-1] * RUDDER_GAIN + RUDDER_OFFSET
    df['thrust'] = ch[:,THRUST_CHANNEL-1] * THRUST_GAIN + THRUST_OFFSET
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='RC output CSV log')
    parser.add_argument('outfile', help='CSV output file name', nargs='?')
    parser.add_argument('--plot', help='flag to enable plot', action='store_true')
    args = parser.parse_args()

    src = pandas.read_csv(args.file, sep=';')

    ch = parse_channels(src['channels'])
    time = src[['time_stamp', 'seq', 'secs', 'nsecs']].copy()
    out = pandas.concat([time, ch], axis=1)

    # write CSV
    if args.outfile is not None:
        out.to_csv(args.outfile, sep=';')
        print('wrote {} lines to {}'.format(len(out)+1, args.outfile))

    # plot
    if args.plot:
        out[['flaps','aileron','rudder','thrust']].plot(drawstyle='steps')
        plt.show()


if __name__ == '__main__':
    main()