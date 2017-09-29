# gamevids.ai

Summarising videogame videos (selecting frames which will form a short preview) with help of neural networks
=========================================================

Creating video input sequences to train networks
------------------------------------------------------------
initiated by methods from **VideoFetcher.py**<br>
you need to set up parameters for connection to certain Mongo databse with player data in **settings.py**<br>
every next video in sequence must contain vids with max hashtag-based Jaccard similarity form **similarities.py**<br>

Neural networks to use
-----------------------------------------------

Currently we work with GoogleNet or newer Inception, Resnet as pre-selection and as video cutting tool vsLSTM and dppLSTM from zhang2016video


@inproceedings{zhang2016video,
  title={Video summarization with long short-term memory},
  author={Zhang, Ke and Chao, Wei-Lun and Sha, Fei and Grauman, Kristen},
  booktitle={ECCV},
  year={2016},
  organization={Springer}
}


