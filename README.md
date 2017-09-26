# gamevids.ai

Summarising videogame videos (slecting frames which will form a short preview) with help of neural networks
=========================================================

Creating video input sequences to train networks
------------------------------------------------------------
initiated by methods from **VideoFetcher.py**<br>
you need to set up parameters for connection to certain Mongo databse with player data in **settings.py**<br>
each sequence must contain vids with hashtag-based Jaccard similarity not less than 0.75, share of frames with likes/views ration higher than others by threshold margin(0.25) should not exceed 15%

Neural networks to use
-----------------------------------------------

Currently we work with GoogleNet, vsLSTM and dppLSTM from zhang2016video and AlexNet


@inproceedings{zhang2016video,
  title={Video summarization with long short-term memory},
  author={Zhang, Ke and Chao, Wei-Lun and Sha, Fei and Grauman, Kristen},
  booktitle={ECCV},
  year={2016},
  organization={Springer}
}


