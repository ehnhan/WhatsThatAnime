import sys
import re

# get source from https://www.reddit.com/r/anime/wiki/commentfacesources
# commentfacesources.txt is a somewhat cleaned up version of the webpage
# use the sorted section

# modify file so that it is in the format:
# ###Akame ga Kill:
#
# [](#sayhwatagain) #sayhwatagain, [](#shock) #shock

# needed to modify some of the sources ie.
# ###Chihayafuru
# (missing ':')

filename = sys.argv[1]
tracefile = open(filename, "r")
newfile = open("output_sources.txt", "w")

while True:
	line = tracefile.readline()

	if line == "":
		break

	if len(line) > 3 and line[0:3] == "###":
		split = line.split(":")
		newfile.write(split[0][3:] + "\n")
