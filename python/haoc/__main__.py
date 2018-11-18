"""Entry point for standalone operation of headless AoC."""

import argparse
import logging
import os

from haoc import HeadlessAOC


if __name__ == '__main__':
    """Entry point."""
    logging.basicConfig(level='INFO')
    parser = argparse.ArgumentParser()
    parser.add_argument('rec_path')
    parser.add_argument('-i', '--install-path', default='~')
    parser.add_argument('-v', '--visible', action='store_true')
    args = parser.parse_args()
    aoc_path = os.path.expanduser(os.path.join(
        args.install_path,
        '.wine/drive_c/Program Files (x86)/Microsoft Games/Age of Empires II'
    ))
    result = HeadlessAOC(aoc_path, args.rec_path, visible=args.visible).play()
    print(result)
