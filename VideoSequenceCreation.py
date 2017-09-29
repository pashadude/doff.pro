import mongoTools
import smilarities
import VideoProcessing
import argparse

#TODO add selection mechs after amazon server productivity comparison
def main():
    parser = argparse.ArgumentParser(prog='VIDEO SEQUENCE')
    parser.add_argument('game', nargs=1, type=str)
    parser.add_argument('-sequence_length', narga='+', type=int, default=7, const=7)
    args = parser.parse_args()


if __name__ == "__main__":
    main()
