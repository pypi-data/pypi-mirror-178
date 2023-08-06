#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os

from collections import deque
from pathlib import Path
# from logger import logger
from pycap2low.logger import logger


def main():
    # arg_path = '/home/alex/Web/'
    # arg_recursive = False
    # arg_str_camel_case = '-'

    args = _parse_args()
    arg_path = str(Path(args.path).resolve())
    arg_str_camel_case = args.str_camel_case
    arg_recursive = args.recursive

    if not os.path.exists(arg_path):
        msg = 'Invalid directory path'
        logger.error(msg)
        raise ValueError(msg)

    if arg_path == os.getcwd():
        msg = 'The directory must be different from the current one'
        logger.error(msg)
        raise ValueError(msg)

    if not arg_recursive:
        __ren_listdir__(arg_path, str_camel_case=arg_str_camel_case)
    else:
        __ren_listdir_rec__(arg_path, str_camel_case=arg_str_camel_case)

def _parse_args():
    parser = argparse.ArgumentParser(prog='pycap2low',
                                     description='Convert all file and directory names to lower case')

    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%(prog)s 2.0.0')
    parser.add_argument('-a',
                        '--author',
                        action='version',
                        version='%(prog)s was created by software developer Alexis Torres Valdes <alexisdevsol@gmail.com>',
                        help="Show program's author and exit")

    parser.add_argument('path', help='Path of the directory to rename')
    parser.add_argument('-r',
                        '--recursive',
                        action='store_true',
                        help='Apply changes recursively to subdirectories')
    parser.add_argument('--str-camel-case',
                        required=False,
                        help='camel case separator chain')
                        
    return parser.parse_args()

def _lower(txt: str):
    return txt.lower()

def _rep_camel_case(txt: str, strr='-'):
    txtr = ''

    for i in range(len(txt) - 1):
        char = str(txt[i])
        camel_case = char.islower() and str(txt[i + 1]).isupper()
        if camel_case:
            txtr += char.lower() + strr
            continue
        txtr += char.lower()
    if txtr != '':
        txtr += str(txt[len(txt) - 1]).lower()

    return txtr

def __ren_listdir_rec__(path, str_camel_case=None):
    func_ren = _lower if not str_camel_case else _rep_camel_case
    q = deque([path])
    while len(q):
        _path = q.popleft()
        for item in os.listdir(_path):
            p = os.path.join(_path, item)
            new_path = __rename__(p, func_ren)            
            if os.path.isdir(new_path):
                q.append(new_path)
    __rename__(path , func_ren)

def __ren_listdir__(path, str_camel_case=None):
    func_ren = _lower if not str_camel_case else _rep_camel_case
    for item in os.listdir(path):
        __rename__(os.path.join(path, item), func_ren)
    __rename__(path, func_ren)

def __rename__(path: str, func_ren):
    i = path.rfind('/')
    name = path[i + 1:]
    new_path = os.path.join(path[:i], func_ren(name))
    if not os.path.exists(new_path):
        os.rename(path, new_path)
        logger.info("Renamed '%s' => '%s'" % (path, new_path))
        return new_path
    logger.info("Not renamed '%s'" % path)
    return new_path

if __name__ == '__main__':
    main()