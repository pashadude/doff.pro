import mongoTools
import smilarities
import VideoProcessing
import argparse

#TODO add selection mechs after amazon server productivity comparison
def main():
    parser = argparse.ArgumentParser(prog='VIDEO SEQUENCE')
    parser.add_argument('game', nargs=1, type=str)
    parser.add_argument('--seq_min_len', nargs=1, type=int, default=5, const=5)
    args = parser.parse_args()

class VideoSequenceCreation:
    def __init__(self, game, length):
        self.game = game
        self.length = length
        self.video_ids = []

    def make_sequence(self):
        return

    def cut_sequence(self):
        return

if __name__ == "__main__":
    main()
