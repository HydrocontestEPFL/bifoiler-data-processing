import pandas
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', help='CSV file')
args = parser.parse_args()

# get time column
df = pandas.read_csv(args.file, sep=';')
data = df[['secs']].values[:,0]

# calculate reference date
start = datetime.datetime.fromtimestamp(data[0])
stop = datetime.datetime.fromtimestamp(data[-1])

print('start: {}'.format(start))
print('stop:  {}'.format(stop))
