#!/usr/bin/env python3

import os
import sys
import time

import common


def main():
    if not os.path.exists(common.CORPUS_DIR):
        print("Please run `python3 fetch_corpus.py` first to fetch the corpus.")
        sys.exit(1)
        return

    if not os.path.exists(common.LIBS_DIR):
        print("Please run fetch_dependencies.sh first to fetch the necessary tools.")
        sys.exit(1)
        return

    project = ""
    if len(sys.argv) == 2:
        project = sys.argv[1]
    else:
        print('must supply single test name')
        sys.exit()

    print("Running analysis on corpus.")
    print(time.strftime('%X %x'))
    tools = ['randoop']

    print("Cleaning {}".format(project))
    common.clean_project(project)
    common.run_dljc(project, tools)
    print(time.strftime('%X %x'))


if __name__ == "__main__":
    main()
else:
    print('huh?')
