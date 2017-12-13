# gamevids.ai

Summarising videogame videos (selecting frames which will form a short preview) with help of neural networks
=========================================================

Creating video input sequences to train networks
------------------------------------------------------------

1. Select games which videos you would like to parse from www.plays.tv with **GameStatsParser.py**<br>
>python GameStatsParser.py "League of Legends"
2. Download stats about top n videos and write them down to MongoDb with store_game_videos method in **VideoStatsFetcher**<br>
you need to set up parameters for connection to certain Mongo databse with player data in **settings.py**<br>
>python VideoStatsFetcher.py "League of Legends" 900
3. Create Graph of similar videos (nodes are the videos, connections are jaccard similarites higher than certain threshold, currently 0.5)<br>
and save it in py2neo/neo4j format with fill_similarities_graph method in **VideoStatsFetcher**<br>
4. Create a dataframe containing all video Id's and ratings for each video sequence with **VideoSequenceCreation.py**, by default 4 vids in a sequence<br>
every next video in sequence must be the one with the highest hashtag-based Jaccard similarity form **similarities.py**<br>
>python VideoSequenceCreation.py "League of Legends"
5. Take frames from a particular video sequence(s) and assign rating to each frame **VideoProcessing.py** <br>
>python VideoProcessing.py "League of Legends" "0, 1"
6. Feed frames to your neural network <br>
7. Train your network. Currently we work with GoogleNet or newer Inception, Resnet as pre-selection and as video cutting tool vsLSTM and dppLSTM from zhang2016video <br>

--------------------------------------------------------------
we use deep learning ami with sc cuda-9 ubuntu



