# WhatsThatAnime
Chrome extension that displays sources for commentfaces on the anime subreddit

# Files
us.json is from http://bcmoe.blob.core.windows.net/assets/us.json

pygoogle.py is from https://code.google.com/archive/p/pygoogle/

# Modifications
To get the output of sources from image_to_source parser to be unique and sorted:

sort outputsources.txt | uniq > out.txt

Look in commentfaces_to_modify.txt to find where in the output of image_to_source parser you need to change manually
