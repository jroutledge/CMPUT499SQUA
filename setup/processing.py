#!/usr/bin/python3
import os
import subprocess


class Processor:
    """
    Processor class to create final word lists for
    a given grade level
    """

    def __init__(self, gradeLevel, outputFile, pathToWordLists):
        """ """
        self.gradeLevel = str(gradeLevel)           # grade level desired for list to be compiled
        self.outputFileName = outputFile            # name of file to output the list to
        self.outputFile = None                      # file pointer
        self.path = str(pathToWordLists)
        self.words = []

    def start(self):
        """ start processing """
        self.outputFile = open(self.outputFileName, "w")
        # put all the words from the files into an array
        self.process_folders()
        self.process_words()

    def end(self):
        """ clean up and end processing """
        self.outputFile.close()

    def process_words(self):
        # sort words
        self.words.sort()
        # print(self.words)
        # get duplicate words
        words = self.words
        duplicates = set([x for x in words if words.count(x) > 1])
        print(duplicates)
        print(len(duplicates))

    def process_folders(self):
        # get folder names
        folders = os.listdir(self.path + "/word_lists")

        for folder in folders:

            fname = self.path + "/word_lists/" + folder + "/Grade" + self.gradeLevel + ".txt"
            f = open(fname, "r")

            # get all the words from each file
            for line in f:
                line = line.rstrip()
                if line != "":
                    self.words.append(line)

            f.close()


def test():
    for grade_level in range(1, 9):
        p = Processor(grade_level, "test_output.txt", os.getcwd())
        print("---------------------------------------------------")
        print("STARTING GRADE LEVEL ", grade_level)
        print("---------------------------------------------------")

        p.start()
        p.end()


if __name__ == "__main__":
    test()
