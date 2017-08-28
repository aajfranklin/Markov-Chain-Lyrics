"""

RADIOHEAD MARKOV:
Pick your album(s) and a single word to generate a new "Radiohead" song

"""

#imports modules
from markov_python.cc_markov import MarkovChain
from urls import albums
from fetch_lyrics import fetch
import time
import win32com.client as wincl



#function takes input from user, checks the input against a list of valid inputs, and prompts the user again if their input is invalid
def validated_input(prompt, valid_values):
    valid_input = False
    while not valid_input:
        value = raw_input(prompt)
        if value.lower() not in valid_values:
        	print("Sorry, that input was not valid. Please try again.")
        valid_input = value.lower() in valid_values
    return value

#function prompts the user to choose albums to emulate and outputs list of indices corresponding to album dictionary indices in urls.py
def choose():
	selections = []
	print("\nOK, first pick the album(s) you want to emulate: \n")
	time.sleep(2)
	for i in range(len(menu)):
		print(menu[i][1])
	while True:
		while True:
			choice = int(validated_input("\nType a number from 0-9 to choose an album: ", [str(x) for x in range(10) if x not in selections]))
			cont1 = validated_input("\nYou chose %s, is that correct (y/n)? " %(menu[choice][1][4:]), ["y","n"])
			if cont1 == "n":
				print("\nOK, please reselect the album you want.")
			else:
				break
		if choice == 0:
			selections = [1,2,3,4,5,6,7,8,9]
			break
		else:
			selections.append(choice)
			cont2 = validated_input("\nWould you like to add another album (y/n)? ", ["y","n"])
			if cont2 == "n":
				break
	return selections

#list of albums for use in the choose function
menu = [
[0,"0 - All Albums"],
[1,"1 - Pablo Honey"],
[2,"2 - The Bends"],
[3,"3 - OK Computer"],
[4,"4 - Kid A"],
[5,"5 - Amnesiac"],
[6,"6 - Hail to the Thief"],
[7,"7 - In Rainbows"],
[8,"8 - The King of Limbs"],
[9,"9 - A Moon Shaped Pool"]
]

#programme introduction
print("\n (^_^)/")
print("\nWelcome! Have you ever wanted to write songs as good as Radiohead's? Well look no further: I can do it for you!")
time.sleep(4)
print("\nJust pick an album whose style you want to emulate and write the first word of your song. I'll do the rest!")
time.sleep(4)
print("\nI regret that I can only handle the lyrics side at this time. Please accept my humblest apologies.")
time.sleep(3)
print(u"\n (\u00B0-\u00B0)")
time.sleep(2)
print("\n_(._.)_ ")
time.sleep(2)
print(u"\n (\u00B0-\u00B0)") 
time.sleep(2)

#while loop determines whether user will generate another song after each use
cont0 = "y"
while cont0 == "y":

	selections = choose()

#displays the user's final selections
	if len(selections) == 9:
		print("\nThank you. You chose All Albums - bold!")
	elif len(selections) == 1:
		print("\nThank you. You chose %s." %([menu[x][1][4:] for x in selections][0]))
	elif len(selections) == 2:
		print("\nThank you. You chose %s and %s." %(menu[selections[0]][1][4:], menu[selections[1]][1][4:]))
	else:
		print("\nThank you. You chose %s, and %s." %(", ".join([menu[x][1][4:] for x in selections[:len(selections)-1]]),menu[selections[len(selections)-1]][1][4:]))

#fetches lyrics for the user's selection, assures user of load time
	time.sleep(1)
	print("\nI'm just fetching the original lyrics for your selection from 'lyrics.wikia.com'. The more albums you chose, the longer this will take.")
	out = fetch(selections)
	print("\nOK, I've loaded the original lyrics.")
	time.sleep(1)

#below we generate the markov chain

#first we assign values for words per song and words per line for later use in the Markov Chain
	num_songs = sum([len(albums[x]) for x in selections])
	num_lines = len(out.splitlines())
	num_words = len(out.split())
	lines_per_song = num_lines/num_songs
	words_per_song = num_words/num_songs
	words_per_line = words_per_song/lines_per_song

#adds album lyrics to Markov chain data
	mc = MarkovChain()
	mc.add_string(out)

#prompts the user for the first word of the song, with the option to view available words, and generate the chain
	time.sleep(1)
	print("\nRight, let's move on to your new song. It's time to write the first word!")
	print("Note that the word has to be in your chosen album(s) original lyrics at least once, else I can't generate a new song from it.")
	print("You can either view the available words, or just try a common song word like 'love' or 'I' to get started.")
	time.sleep(3)
	cont3 = validated_input("\nView available words (y/n)? ", ["y","n"])
	if cont3 == "y":
		print("\n*******************")
		print(" ".join(sorted(set(out.lower().split()))))
		print("*******************")
		time.sleep(1)

	first_word = validated_input("\nWhat would you like the first word to be? ", set(out.lower().split())).lower()
	time.sleep(2)
	chain = mc.generate_text(words_per_song, first_word)

#formats chain to better resemble song lyrics
	song = []

	chain = [word.replace("i'm","I'm") for word in chain]
	chain = [word.replace("i'd","I'd") for word in chain]
	chain = [word.replace("i'll","I'll") for word in chain]
	chain = [word.replace("i've","I've") for word in chain]
	while len(chain) >= words_per_line:
		line = " ".join(chain[:words_per_line])
		line = line.replace(" i ", " I ")
		for ci in range(len(line)-1,-1,-1):
			if ci == len(line)-1 and line[ci] == "i" and line[ci-1] == " ":
				line = line[:len(line)-1] + "I"
		line = line[0].upper() + line[1:]
		chain = chain[words_per_line:]
		song.append(line)

	verse_length = len(song)/5
	song = song[:verse_length*5]

	for i in range(len(song)):
		if (i+1) == len(song):
			song[i] = song[i] + "..."
		elif (i+1) % (verse_length/2) == 0 and i != len(song) - 1:
			song[i] = song[i] + ","

#joins the distinct lines of the song so they can be read by text to speech module
	speak = wincl.Dispatch("SAPI.SpVoice")

#asks the user if they are ready to hear the song
	raw_input("\nOK, your song is ready. Press enter when you are ready to hear it.\n")
	print("\n (^o^) < ...oooOOO000\n")

#prints the song line by line, speaking the lyrics after each verse
	while len(song) >= verse_length:
		for line in song[:verse_length]:
			print(line)
			time.sleep(0.5)
		print("\n")
		speak.Speak(" ".join(song[:verse_length]))
		song = song[verse_length:]

#closing message that reflects the user's selections
	time.sleep(2)
	if len(selections) == 9:
		print("\nWow, just like a song from all Radiohead albums combined... I hope you enjoyed it!")
	elif len(selections) == 1:
		print("\nWow, just like a song from %s... I hope you enjoyed it!\n" %([menu[x][1][4:] for x in selections][0]))
	elif len(selections) == 2:
		print("\nWow, just like a song from %s and %s combined... I hope you enjoyed it!" %(menu[selections[0]][1][4:], menu[selections[1]][1][4:]))
	else:
		print("\nWow, just like a song from %s, and %s combined... I hope you enjoyed it!" %(", ".join([menu[x][1][4:] for x in selections[:len(selections)-1]]),menu[selections[len(selections)-1]][1][4:]))

#prompt the user to generate another song or end the programme
	time.sleep(2)
	cont0 = validated_input("\nWould you like to write another song (y/n)? ", ["y","n"])
	time.sleep(1)

print("\nYes, I think that's enough for now too. Thank you for trying this programme and congratulations on your achievements as a song writer!\n")

"""
TO DO:
add music?
"""


