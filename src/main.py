#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Looking After You, Always. (LAYA)

import os

from features.Core import Bot

def sort_file_paths(source_code: str):
    runpath = os.path.realpath(__file__)
    rundir = runpath[:runpath.find(source_code) + len(source_code) + 1]
    os.chdir(rundir)

def main():
    sort_file_paths(source_code='src')
    bot = Bot()
    bot.initialize()

if __name__ == '__main__':
    main()
