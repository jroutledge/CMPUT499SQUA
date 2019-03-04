import sys
from sys import argv
import os
from os import path

'''This script is to take a finalized list of each grade level and add them into the database'''
def main():
    if len(argv) != 2:
        print("Try harder in the future please")
        sys.exit()
    elif not argv[1].isdigit():
        sys.exit()

    current_path = os.path.dirname(os.path.abspath(__file__))
    f_path = str.format("%s/flocabulary.com/Grade%d.txt" % (current_path, int(argv[1])))
    #TODO: add additional sources

    print(f_path)
    f = open(f_path, 'r')
    cleanList(f)

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

if __name__ == '__main__':
    main()