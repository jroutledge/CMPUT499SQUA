#!/usr/bin/python3
import os


class Processor:
    """
    Processor class to create final word lists for
    a given grade level
    """

    def __init__(self, gradeLevel, outputFile, path):
        """ """
        self.gradeLevel = gradeLevel
        self.outputFile = outputFile
        self.path = path

    def start(self):
        """ start processing """

        # get folder names
        folders = os.listdir(self.path + "/word_lists")
        print(folders)


def main():
    p = Processor(3, "test_output.txt", os.getcwd())
    p.start()


main()
