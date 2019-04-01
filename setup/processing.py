#!/usr/bin/python3
import os
from thesaurus import Word
from thesaurus.exceptions import MisspellingError


class Processor:
    """
    Processor class to create final word lists for
    a given grade level. Processor is set up in a way
    that it will grab anything in the word_lists folders
    to add to each grade level for the data set.
    """

    def __init__(self, gradeLevel, pathToWordLists):
        """
        initialize processor
        """
        self.gradeLevel = str(gradeLevel)           # grade level desired for list to be compiled
        self.outputFileNames = ["table_StartWords.txt",   # name of files to output the lists to
                                "table_SynWords.txt",
                                "table_AntWords.txt"]
        self.outputFiles = None                      # file pointer
        self.path = str(pathToWordLists)
        self.words = []

    def start(self):
        """
        start processing
        """
        # open files
        self.outputFiles = [open(self.outputFileNames[0], "a"),
                            open(self.outputFileNames[1], "a"),
                            open(self.outputFileNames[2], "a")]
        # put all the words from the files into an array
        self.process_folders()
        self.process_words()

    def end(self):
        """
        clean up and end processing
        """
        self.outputFiles[0].close()
        self.outputFiles[1].close()
        self.outputFiles[2].close()

    def process_words(self):
        """
        Sort words, look for duplicates, then get synonyms
        and write to output files. Looking for duplicates
        here because that is an indication that multiple
        sources think the term is appropriate for the
        given grade level.
        """
        # print(self.words)
        # get duplicate words - the words we want to use
        words = self.words
        duplicates = list(set([x for x in words if words.count(x) > 1]))
        duplicates.sort()

        """ try a different way """
        for word in duplicates:
            try:
                w = Word(word)
            except MisspellingError:
                continue
            else:

                # There are 3 relevance levels you can use, 1 will give the set with the most words
                # and possibly some irrelevant words. Here we use 3 to make sure everything stays on topic.
                syns = w.synonyms(relevance=3)

                if syns:
                    for s in syns:
                        self.outputFiles[1].write(word + " " + s + "\n")

                ants = w.antonyms(relevance=3)
                if ants:
                    for a in ants:
                        self.outputFiles[2].write(word + " " + a + "\n")

                if syns or ants:
                    self.outputFiles[0].write(word + " " + self.gradeLevel + "\n")

    def get_synonyms(self, word):
        """
        use nltk to get the synonyms
        """
        return wn.synsets(word)

    def process_folders(self):
        """
        look through folders for word lists of a grade level
        """
        # get folder names
        folders = os.listdir(self.path + "/word_lists")

        for folder in folders:

            fname = self.path + "/word_lists/" + folder + \
                    "/Grade" + self.gradeLevel + ".txt"
            f = open(fname, "r")

            # get all the words from each file
            for line in f:
                line = line.rstrip()
                if line != "":
                    self.words.append(line)

            f.close()


def test():
    print("STARTING PROCESSING")
    for grade_level in range(1, 9):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        p = Processor(grade_level, dirname)
        print("---------------------------------------------------")
        print("STARTING GRADE LEVEL ", grade_level)
        print("---------------------------------------------------")

        p.start()
        p.end()
    print("ENDING PROCESSING")


if __name__ == "__main__":
    test()
