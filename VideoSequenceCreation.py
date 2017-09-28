import mongoTools
import smilarities
import VideoProcessing
import argparse

#TODO add selection mechs after amazon server productivity comparison
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('game', nargs='+', type=str)
    parser.add_argument('sequence_length', type=int)
    parser.add_argument('similarity_threshold', type=double)
    parser.add_argument('')
    args = parser.parse_args()


if __name__ == "__main__":
    main()
