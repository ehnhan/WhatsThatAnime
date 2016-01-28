import sys
import re

filename = sys.argv[1]
tracefile = open(filename, "r")
newfile = open("output.csv", "w")

# get source from https://www.reddit.com/r/anime/wiki/commentfacesources

# modify file so that it is in the format:
# [](#breakingnews)  ^#breakingnews| Love Lab|  [](#brofist) ^#brofist| Ore Monogatari | [](#cokemasterrace) ^#cokemasterrace|  K-On!  |

# needed to modify some of the sources ie. [](#akyuusqueel) ^#akyuusqueel| [Touhou fanart](http://www.pixiv.net/member_illust.php?mode=medium&amp;illust_id=12981879)

while True:
	line = tracefile.readline()

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

		newfile.write(output + "\n")
