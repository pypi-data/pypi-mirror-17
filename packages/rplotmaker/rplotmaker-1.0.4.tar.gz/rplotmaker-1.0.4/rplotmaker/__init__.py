#!/usr/bin/env python
from __future__ import print_function

"""
TODOs:
    - Do not destroy output file if R fails or produces no output
    - Arbitrary arguments support
"""

import argparse
import errno
import fcntl
import logging
import sh
import shutil
import tempfile
import os
from os import path

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_script', type=argparse.FileType('r'),
                   help='Path to read R script from')
    parser.add_argument('output_plot', type=argparse.FileType('a+'),
                   help='Path to store output to')
    parser.add_argument('--width', type=int, default=640,
                   help='Image width [default: 640]')
    parser.add_argument('--height', type=int, default=480,
                   help='Image height [default: 480]')
    parser.add_argument('--background', default='white',
                   help='Image background [default: white]')
    parser.add_argument('--timeout', type=int, default=100,
                help='How long (in seconds) we give to R to compute the image [default: 100]')
    parser.add_argument('--quiet', action='store_true',
                help='Swallow log output')
    return parser

def lock_output(f):
    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as e:
        if e.errno in (errno.EACCES, errno.EAGAIN):
            return False
        raise
    return True

def wait_until_unlocked(f):
    fcntl.lockf(f, fcntl.LOCK_SH)

def atomically_replace_destination(source_path, destination_file):
    if 'nt' == os.name:
        # os.rename is not atomic on windows, and raises if target file is already available
        destination_file.seek(0)
        destination_file.truncate()
        shutil.copy(source_path, destination_file.name)
        os.unlink(source_path)
        return
    
    os.rename(source_path, destination_file.name) # atomic

def is_empty_or_not_existant(a_path):
    if not path.exists(a_path):
        return True
    
    info = os.stat(a_path)
    return info.st_size == 0

def main(override_arguments=None):
    logging.getLogger().setLevel(logging.INFO)
    args = argparser().parse_args(args=override_arguments)
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    if not lock_output(args.output_plot):
        logging.info("Output file is already locked, subscribing to result.")
        wait_until_unlocked(args.output_plot)
        logging.info("Output file is now unlocked, plot should be available.")
        return
    
    logging.info("Locked output file.")
    
    rstudio_script = args.input_script.read()
    temp_dir = tempfile.mkdtemp()
    temp_output = path.join(temp_dir, 'output.png')
    
    r_output_setup = '''png(filename="{filename}", width={width}, height={height}, bg="{background}")'''.format(
        filename=temp_output,
        background=args.background,
        width=args.width,
        height=args.height,
    )
    r_script = """%s\n%s\n""" % (r_output_setup, rstudio_script)
    
    # open r interpreter via suprocess (or the subprocess callout thing we use)
    try:
        logging.info("Starting R process.")
        result = sh.R(no_save=True, slave=True, _in=r_script, _err_to_out=True, _timeout=args.timeout)
        logging.info("R succeeded: %s\n%s" % (result.stdout, result.stderr))
    except sh.ErrorReturnCode as exception:
        logging.warn("R failed: %s\n%s" % (exception.stdout, exception.stderr))
        return
    
    if is_empty_or_not_existant(temp_output):
        return # don't destroy original file
    
    atomically_replace_destination(temp_output, args.output_plot)
    
    os.rmdir(temp_dir)

if __name__ == '__main__':
    main()
