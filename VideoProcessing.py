import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")
import cv2
import settings
import pandas as pd
import argparse
import youtube_dl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('game', nargs=1, type=str)
    def convert(argument):
        return list(map(str, argument.split(', ')))
    parser.add_argument('sequence', nargs='+', type=convert)
    args = parser.parse_args()
    images = SequenceFetcher(args.game[0], args.sequence[0])
    images.make_sequences()

class SequenceFetcher:
    def __init__(self, game, sequences):
        self.game = game
        self.angles = settings.
        self.sequences = sequences
        self.videoSequenceFilePath = '{0}/{1}/sequences.csv'.format(settings.VideosDirPath, self.game)
        print(self.game, self.sequences)

    def make_sequences(self):
        df = pd.read_csv(self.videoSequenceFilePath)
        #print(list(df.columns.values))
        k = 1
        for i in df['sequence']:
            if str(i) in self.sequences:
                vid = self.fetch_video(df['video'][k], i)
                self.split_video_frames(vid, i, df['video'][k], df['rating'][k])
            k+=1
        return

    def fetch_video(self, id, sequence):
        uri = 'http://plays.tv/video/{0}'.format(id)
        #print(cv2.__version__, cv2.__spec__)
        ydl_opts = {
            'format': 'best',
            'preferredcodec': 'mp3',
            'outtmpl': '{0}/{1}/sequence_{2}/{3}.mp4'.format(settings.VideosDirPath, self.game, sequence, id)
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([uri])
        return '{0}/{1}/sequence_{2}/{3}.mp4'.format(settings.VideosDirPath, self.game, sequence, id)

    def split_video_frames(self, videoPath, sequence, video, rating):
        vidcap = cv2.VideoCapture(videoPath)
        success = True
        count = 0
        while success:
            success, image = vidcap.read()
            count+=1

            #self.cut_additional_frames(sequence, int(start + count), rating)
            if cv2.waitKey(10) == 27:
                break
        vidcap.release()
        return

    # need to improve
    def cut_additional_frames(self, sequence, video, frame, rating):
        img = cv2.imread('{0}/{1}/sequence_{2}/seq{2}_vid{3}_frame{4}_full_rating{5}.jpg'.format(settings.VideosDirPath, self.game, sequence, video, frame, rating))
        count = 1
        for k in self.angles:
            crop_img = img[k[0]:299, k[1]:299]
            #crop_img = img[200:400, 100:300]
            cv2.imwrite('{0}/{1}/sequence_{2}/seq{2}_vid{3}_frame{4}_{5}_rating{6}.jpg'.format(settings.VideosDirPath,
                                                                                                self.game, sequence,
                                                                                                video, frame, count, rating),crop_img)
            count += 1
        return

if __name__ == "__main__":
    main()

