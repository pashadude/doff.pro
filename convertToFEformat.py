import h5py
import numpy as np
import ntpath
import sys

class converter:

   def __init__(self):
       self.features =  []
       self.nVideos = 0
       self.nFramesPerVideo = {}
       self.seqId_To_videoId = {}

   def parseFname(self,fname):
       ''' extract
           N-game, m-sequence, I-frame, j-corner, k-rating
           from string fname '''
       # fname has format <name>.<ext>
       #name,sep,ext = fname.partition(".")
       #assert sep is not mpty

       # name has format <game>_<sequence_id>_<frame_id>_<corner>_<rating>
       tokens = fname.split("_")
       if len(tokens)!=4: return None

       # game_id, sequence_id, frame_id, image_corner, frame_rating = tokens
       sequence_id=tokens[0].replace('seq','')
       frame_id=tokens[2].replace('frame','')
       rating=tokens[3].replace('rating-','')
       rating=rating.replace('.jpg','')
       return (int(sequence_id), int(frame_id), float(rating))

   def splitFname(self,filePath_b):
       fname_b = ntpath.basename(filePath_b) # this is a byte array
       fname_s = fname_b.decode()  # this is a string
       return fname_s

   def getVideoId(self, sequence_id):
       if sequence_id in self.seqId_To_videoId:
           video_id = self.seqId_To_videoId[sequence_id]
       else:
           self.seqId_To_videoId[sequence_id] = self.nVideos
           video_id = self.nVideos
           self.nVideos+=1

       return video_id

   def updateNumberOfFrames(self,video_id, frame_id):
       if (video_id not in self.nFramesPerVideo):
          self.nFramesPerVideo[video_id]=frame_id
       else:
          self.nFramesPerVideo[video_id]=max(frame_id, self.nFramesPerVideo[video_id])

   def loadFileWithFeatures(self,filename, features_key = "Logits"):
       print("Loading file ", filename)

       self.inputFileName = filename
       self.input_file = h5py.File(filename, "r")
       self.features_key=features_key

       self.nFeatures = self.input_file.get(features_key).shape[1]
       self.image_fullnames = np.array(self.input_file.get('filenames'))

       for idx, fpath in enumerate(self.image_fullnames):
           fname = self.splitFname(fpath)
           tokens = self.parseFname(fname)
           if tokens is None:
               continue
           sequence_id, frame_id, frame_rating = tokens

           # unique identifier of a "video" is <sequence_id>
           # Find out: 
           #   map <sequence_id> to a unique linear index 
           #   compute number of frames and number of corners per frame for each <sequence_id>

           video_id = self.getVideoId(sequence_id)
           self.updateNumberOfFrames(video_id, frame_id)


   def initializeOutput(self, lstmFile):
      ''' format is :
           for each video there are 3 matrices fea_<i>, gt_1_<i>, gt_2<i> where <i> is the index of a video
               - fea_<i> :: features stored in matrix <number_of_features> x <number_of_frames>
               - gt_1_<i>:: importance of each frame <number_of_frames> x 1
               - gt_2_<i>:: binary flag indicating if frame ended up being selected or not <number_of_frames> x 1
           idx : the index of videos :: just list of indices, doesn't look like its used by data loader
                 <number_of_videos> x 1
           ord : unknown, looks like an ordering of the video indices, appears to be unused
      '''
      for video_id in range(0, self.nVideos):
          # dimensions = <number_of_features> x <number_of_frames> 
          number_of_frames = self.nFramesPerVideo[video_id]+1

          lstmFile.create_dataset('fea_'+str(video_id), (self.nFeatures, number_of_frames))
          lstmFile.create_dataset('gt_1_'+str(video_id), (number_of_frames,1))

          lstmFile.create_dataset('gt_2_'+str(video_id),(number_of_frames,1))  # unused
          #lstmFile.create_dataset('ord'+str(video_id),(number_of_frames,1))   # unused


   def writeInputForLSTM4VS(self,output_name):
      lstmFile = h5py.File(output_name,"w")
      self.initializeOutput(lstmFile)

      self.features = np.array(self.input_file.get(self.features_key))

      for feature_row, fpath in zip(self.features, self.image_fullnames):
           # read corresponding file name again
           fname = self.splitFname(fpath)
           sequence_id, frame_id, frame_rating = self.parseFname(fname)
           # where does this row of features go into output file?
           # into fea_<video_id> column <frame_id> and within column into position corner*len(feature_row)
           video_id = self.getVideoId(sequence_id)

           feature_set = lstmFile.get('fea_'+str(video_id))
           feature_set[:, frame_id] = feature_row

           rating_set = lstmFile.get('gt_1_'+str(video_id))
           rating_set[frame_id] = frame_rating

      lstmFile.close()
      self.input_file.close()


if __name__=="__main__":
    nArgs = len(sys.argv)
    assert nArgs == 3
    input_fname = sys.argv[1]
    output_fname = sys.argv[2]

    print("input name :", input_fname)
    print("output name :", output_fname)

    cnv = converter()
    cnv.loadFileWithFeatures(input_fname)
    cnv.writeInputForLSTM4VS(output_fname)
