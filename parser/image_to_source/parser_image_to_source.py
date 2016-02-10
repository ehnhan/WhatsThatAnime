import sys
import re

# get source from https://www.reddit.com/r/anime/wiki/commentfacesources
# commentfacesources.txt is a somewhat cleaned up version of the webpage
# (use the no order section)

# modify file so that it is in the format:
# [](#breakingnews)  ^#breakingnews| Love Lab|  [](#brofist) ^#brofist| Ore Monogatari

# needed to modify some of the sources
# ie. [](#akyuusqueel) ^#akyuusqueel| [Touhou fanart](http://www.pixiv.net/member_illust.php?mode=medium&amp;illust_id=12981879)

inputfile = open("input_image_to_source.txt", "r")
outputfile = open("output_image_to_source.csv", "w")

outputShows = open("outputsources.txt", "w")

# sources_to_modify.txt contains names of sources that need to be changed to match the titles used in our streaming site json file in our other parser
changefile = open("sources_to_modify.txt", "r")
changeMap = dict()

# create a map of the names that need to be changed
while True:
	line = changefile.readline()

	if line == "":
		break

	split = line.split(" = ")
	changeMap[split[0]] = split[1]

while True:
	line = inputfile.readline()

	if line == "":
		break

	# separate lines
	regex0 = re.compile('\[.*?\)')
	split = regex0.split(line)

	for source in split:
		if source == "" or source == "\n":
			continue

		# remove ^
	 	regex1 = re.compile('\^')
		clean1 = regex1.sub("", source)

		# remove | at the ends and replace middle | with ,
		regex2 = re.compile('\|')
		clean2 = regex2.split(clean1)

		# trim whitespace from front and end
		output = clean2[0].strip() + "," + clean2[1].strip()

		# replace name if needed
		splitShow = output.split(',', 1)
		newName = changeMap.get(splitShow[1])
		if newName != None and newName != "NOT FOUND\n":
			outputShows.write(newName)
			outputfile.write(splitShow[0] + "," + newName)
		else:
			outputShows.write(splitShow[1] + "\n")
			outputfile.write(output + "\n")
