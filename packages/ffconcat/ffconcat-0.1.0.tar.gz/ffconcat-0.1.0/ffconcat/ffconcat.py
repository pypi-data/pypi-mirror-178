#!/usr/bin/env python
# coding: utf-8

import argparse
import sys
from pathlib import Path

import ffmpeg


def opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help='Paths to the video files')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        help='Name of the output file',
                        required=True)
    parser.add_argument(
        '-c',
        '--codec',
        type=str,
        help='Defaults to `copy` when all input files have the same extension; '
        'otherwise, defaults to `libx265`')

    return parser.parse_args()


def main():
    args = opts()
    input_files = [f'file {x}\n' for x in args.input]
    tmp_file = '.ffconcat'
    with open(tmp_file, 'w') as f:
        f.writelines(input_files)

    same_ext = len(set(Path(x).suffix for x in input_files)) == 1

    if same_ext and not args.codec:
        codec = 'copy'
    elif not same_ext and args.codec == 'copy':
        sys.exit('Cannot use `copy` when the files have different extensions.')
    elif not same_ext and not args.codec:
        codec = 'libx265'
    else:
        codec = args.codec

    try:
        ffmpeg.input(tmp_file, f='concat',
                     safe='0').output(args.output, codec='copy').run()
    except Exception as e:
        print(e)
    finally:
        Path(tmp_file).unlink()


if __name__ == '__main__':
    main()
