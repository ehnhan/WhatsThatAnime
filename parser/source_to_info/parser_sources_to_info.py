import sys
import re
import json
from pygoogle import pygoogle

# Got input_shows.txt from image_to_source parser
# Need to format outputsources.txt and remove duplicates
# *** Don't use sources parser, it is missing some sources

# Get us.json from:
# http://bcmoe.blob.core.windows.net/assets/us.json

# TODO test on smaller file
inputfile = open("sample.txt", "r")
#inputfile = open("input_shows.txt", "r")

newfile = open("output_sources_to_info.json", "w")

json_data = open("us.json")
watch_obj = json.load(json_data)['shows']

output = "{\"shows\": ["

while True:
	line = inputfile.readline()

	if line == "":
		break

 	line = line.replace('\n', '')

	# start line for a show
	output += "{\"name\": \"" + line + "\", \"sites\": {"

	# TODO
	# USE other api instead because google limited to 100 searches/day
	# find the myanimelist and wikipedia page for the show
	g = pygoogle(line)
	g.pages = 1
	sites = g.get_urls()

	myanime = ""
	wiki = ""

	foundInfo = True

	# find the wikipedia and myanimelist urls from the results
	for link in sites:
		if "http://myanimelist.net/" in link.lower():
			myanime = link
		if "https://en.wikipedia.org/" in link.lower():
			wiki = link

	# add info sites to output
	if (myanime != "") and (wiki != ""):
		output += "\"info\": {\"myanimelist\": \"" + myanime + "\", \"wikipedia\": \"" + wiki + "\"}, "
	elif (myanime != ""):
		output += "\"info\": {\"myanimelist\": \"" + myanime + "\"}, "
	elif (wiki != ""):
		output += "\"info\": {\"wikipedia\": \"" + wiki + "\"}, "
	else:
		foundInfo = False

	# find the streaming sites for the show
	foundStream = False
	for show in watch_obj:
		if show['name'] == line:
			streams = json.dumps(show['sites'])
			output += "\"streams\": " + streams
			foundStream = True

	if not foundStream and foundInfo:
		# remove ", " from end because no streams
		output = output[:-2]

	# close a line for a show
	output += "}}, "

# remove ", " from end
output = output[:-2]
output += "]}"

newfile.write(output)

json_data.close()
