#contains code to fetch lyric text data

#import modules
from urls import albums
import urllib2

def fetch(lst):
	out = ""
	for x in lst:
		for song in albums[x]:
			
			#imports html file from url for the song
			html_doc = urllib2.urlopen(song)
			
			#imports html file from URL
			raw = str(html_doc.read())
			
			#identifies the portion of the file that contains song lyrics
			header = "</h1>"
			raw = raw[raw.find(header,0):]
			lyric_head = ";lyrics>"
			lyric_foot = "/lyrics>"
			start = 8 + raw.find(lyric_head, 0)
			end = raw.find(lyric_foot) - 4
			lyrics = raw[start:end]
			
			#removes undesired words, punctuation, or html formatting from lyrics
			strings_to_cut = [
			"{{Instrumental}}",
			"''",
			'"',
			"(",
			")",
			"?",
			"...",
			","
			]

			for x in strings_to_cut:
				lyrics = lyrics.replace(x,"")


			#appends the lyrics to the output
			out += lyrics

	return out
