#!/usr/bin/python3
"""
This script is to take a finalized list of each grade level and add
them into the database
"""

import sys
from sys import argv
import os
from processing import Processor
from create_db import Creator


def cleanList(f):
    words = f.readlines()

    to_pop = []
    for i in range(0, len(words)):
        word = words[i]
        word = word.rstrip().lower()
        if word == "":
            to_pop.append(i)
        print(word)
        words[i] = word

    num_popped = 0
    for i in to_pop:
        words.pop(i-num_popped)
        num_popped+=1

    print(words)
    return words


def main():

    if len(argv) != 2:
        print("Try harder in the future please")
        sys.exit()
    elif not argv[1].isdigit():
        sys.exit()

    current_path, filename = os.path.split(os.path.abspath(__file__))
    # f_path = str.format("%s/flocabulary.com/Grade%d.txt" % (current_path, int(argv[1])))
    # TODO: add additional sources
    # print(f_path)
    # f = open(f_path, 'r')
    # cleanList(f)

    # run processor
    dir = os.listdir(current_path)
    # check to see if the files needed are available
    # if they are not, then we run the processor
    # otherwise we skip this step
    # note, running the processor takes around 3 minutes
    if "table_StartWords.txt" not in dir or "table_SynWords.txt" \
            not in dir or "table_AntWords.txt" not in dir:

        for grade_level in range(1, 9):
            p = Processor(grade_level, current_path)
            print("Processing grade level " + str(grade_level))
            p.start()
            p.end()

    # now we add the things to the database
    db_create = Creator(current_path)
    db_create.create_tables()
    db_create.populate()
    db_create.end()


if __name__ == '__main__':
    main()
