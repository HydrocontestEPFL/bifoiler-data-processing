import pandas
import datetime
import argparse
import os
import itertools

def time_index(time_data, t_ref):
    if t_ref is not None:
        for i in range(len(time_data)):
            if time_data[i] >= t_ref:
                return i;

    return len(time_data)-1

def get_timestamps(filename, start, stop):
    # get time column
    df = pandas.read_csv(filename, sep=';')
    data = df[['secs']].values[:,0]

    # calculate reference date
    day = datetime.datetime.fromtimestamp(data[0]).date()

    # add time of day
    starttime = datetime.datetime.strptime(start, '%H:%M:%S').time()
    start = datetime.datetime.combine(day, starttime)

    # add time of day
    stoptime = datetime.datetime.strptime(stop, '%H:%M:%S').time()
    stop = datetime.datetime.combine(day, stoptime)

    return start.timestamp(), stop.timestamp()

def get_index(filename, start, stop):
    # get time column
    df = pandas.read_csv(filename, sep=';')
    data = df[['secs']].values[:,0]

    istart = time_index(data, start)
    istop = time_index(data, stop)
    return istart, istop

def extract_lines(file, istart, istop, outfile):
    src = open(file, 'rt')
    dest = open(outfile, 'wt')

    # copy CSV header
    dest.write(next(src))

    count = 0
    # copy range of lines
    for line in itertools.islice(src, istart, istop):
        count += 1
        dest.write(line)

    src.close()
    dest.close()

    print('wrote {} lines to {}'.format(count, outfile))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outdir', default='out', help='output directory name')
    parser.add_argument('start', type=str, help='start time in format hh:mm:ss')
    parser.add_argument('stop', type=str, help='stop time in format hh:mm:ss')
    parser.add_argument('files', nargs='+', help='CSV files')
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    start, stop = get_timestamps(args.files[0], args.start, args.stop)

    for file in args.files:
        istart, istop = get_index(file, start, stop)
        outfile = os.path.join(args.outdir, os.path.basename(file))
        extract_lines(file, istart, istop, outfile)

if __name__ == '__main__':
    main()