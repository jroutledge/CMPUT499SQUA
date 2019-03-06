""" meant for formatting word lists before processing """


def main():
    """ """
    files = ["Grade1.txt", "Grade2.txt", "Grade3.txt", "Grade4.txt", "Grade5.txt", "Grade6.txt", "Grade7.txt", "Grade8.txt"]

    for name in files:
        # f_name = "word_lists/aaaspell.com/" + name
        f_name = "word_lists/greatschools.org/" + name
        f = open(f_name, "r")

        lines = f.readlines()
        to_write = []
        for l in lines:
            l = l.rstrip()
            if l != "":
                l = l.split()
                for word in l:
                    to_write.append(word)
        f.close()
        f = open(f_name, "w")
        for word in to_write:
            f.write(str(word) + "\n")


if __name__ == "__main__":
    main()