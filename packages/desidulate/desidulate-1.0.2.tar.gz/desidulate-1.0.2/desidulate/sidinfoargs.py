#!/usr/bin/python3

import argparse
import os
import re
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hvscdir', default='.', type=str)
    parser.add_argument('--ext', default='', type=str)
    parser.add_argument('--filter', default='', type=str)
    timer_parser = parser.add_mutually_exclusive_group(required=False)
    timer_parser.add_argument('--timer', dest='timer', action='store_true', default=True, help='add timer args')
    timer_parser.add_argument('--no-timer', dest='timer', action='store_false', help='do not add timer args')
    args = parser.parse_args()

    filter_re = None
    if args.filter:
        filter_re = re.compile(args.filter)

    timerflag = {0: 'ntsc', 1: 'pal'}
    df = pd.read_csv(os.path.join(args.hvscdir, 'sidinfo.csv'), usecols=['path', 'magicID', 'sids', 'pal', 'cia'])
    df = df[(df.magicID == 'PSID') & (df.sids == 1)]
    outputs = []
    for row in df.itertuples():
        filename = os.path.normpath(row.path)
        filename = filename[:filename.find('.')]
        if filter_re and not filter_re.match(filename):
            continue
        if args.ext:
            filename = '.'.join((filename, args.ext))
        try:
            size = os.path.getsize(filename)
        except OSError:
            continue
        if args.timer:
            if row.cia:
                cia = row.cia
            else:
                cia = 0
            sidinfo_args = ' '.join(['--%s' % timerflag[row.pal], '--cia=%u' % cia, filename])
        else:
            sidinfo_args = filename
        outputs.append((size, sidinfo_args))

    for _size, sidinfo_args in sorted(outputs, reverse=True):
        print(sidinfo_args)


if __name__ == '__main__':
    main()
