import os
import cv2
import settings
import youtube_dl

class SequenceFetcher:
    def __init__(self, uri, game, videoids, sequence):
        self.uri = uri
        self.game = game
        self.ids = videoids
        self.sequence = sequence
        self.videoFolderPath = '{0}/{1}/{2}'.format(settings.VideosDirPath, self.game, self.sequence)

    def fetch_video(self, id):
        print(cv2.__version__, cv2.__spec__)
        ydl_opts = {
            'format': 'best',
            'preferredcodec': 'mp3',
            'outtmpl': '{0}/videos/{1}.mp4'.format(self.videoFolderPath, id)
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.uri])
        return '{0}/videos/{1}.mp4'.format(self.videoFolderPath, id)

    def split_video_frames(self, videoPath, sequence, label, id):
        vidcap = cv2.VideoCapture(videoPath)
        count = 0
        success = True
        while success:
            success, image = vidcap.read()
            cv2.imwrite('{0}/{1}/{2}_frame{3}.jpg'.format(self.videoFolderPath, label, id, count), image)
            if cv2.waitKey(10) == 27:
                break
            count += 1
        return count



