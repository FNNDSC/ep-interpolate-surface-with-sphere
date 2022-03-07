#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from typing import BinaryIO, Sequence, Literal, Optional
import subprocess
from loguru import logger
from chris_plugin import chris_plugin, PathMapper
from civet.extraction import Side, IrregularSurface

SIDE_OPTIONS = ('left', 'right', 'auto', 'none')
SideStr = Literal['left', 'right', 'auto', 'none']


parser = ArgumentParser(description='Resample surface mesh to have 81,920 triangles.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--side', default='auto', choices=SIDE_OPTIONS,
                    help='brain hemisphere side. "auto" => infer from file name')
parser.add_argument('-p', '--pattern', default='**/*.obj',
                    help='pattern for file names to include')
parser.add_argument('-q', '--quiet', action='store_true',
                    help='disable status messages')
parser.add_argument('--no-fail', action='store_true', dest='no_fail',
                    help='do not produce non-zero exit status on failures')


def isws(surface: Path, output: Path, side: SideStr) -> None:
    log_path = output.with_suffix('.log')
    try:
        logger.info('Processing {} to {}, log: {}', surface, output, log_path)
        with log_path.open('wb') as log:
            IrregularSurface(surface)\
                .interpolate_with_sphere(pick_side(surface, side))\
                .save(output, shell=curry_log(log))
        logger.info('Completed {}', output)
    except Exception as e:
        logger.exception('Failed to process {}', surface)
        raise e


def curry_log(log: BinaryIO):
    def run_with_log(cmd: Sequence[str | os.PathLike]) -> None:
        subprocess.run(cmd, stderr=log, stdout=log, check=True)
    return run_with_log


def pick_side(input_path: Path, side: SideStr) -> Optional[Side]:
    if side == 'left':
        return Side.LEFT
    if side == 'right':
        return Side.RIGHT
    if side == 'auto':
        path = str(input_path).lower()
        if 'left' in path:
            return Side.LEFT
        if 'right' in path:
            return Side.RIGHT
        raise ValueError(f'Substring "left" nor "right" found in: {path}')
    if side == 'none':
        return None
    raise ValueError(f'side must be one of: {SIDE_OPTIONS}')


@chris_plugin(
    parser=parser,
    category='MRI Processing',
    min_memory_limit='100Mi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    if options.quiet:
        logger.remove()
        logger.add(sys.stderr, level='WARNING')

    nproc = len(os.sched_getaffinity(0))
    logger.debug('Using {} threads.', nproc)

    results = []
    with ThreadPoolExecutor(max_workers=nproc) as pool:
        mapper = PathMapper(inputdir, outputdir, glob=options.pattern, suffix='._81920.obj')
        for mc_surface, output in mapper:
            results.append(pool.submit(isws, mc_surface, output, options.side))

    if options.no_fail:
        return
    for future in results:
        e = future.exception()
        if e is not None:
            raise e


if __name__ == '__main__':
    main()
