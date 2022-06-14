from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE", type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    print(args.filename == None)